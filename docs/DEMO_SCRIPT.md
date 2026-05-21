# Demo Script — AttestRWA

Two versions: a tight 90-second main pitch and a 3-minute extended for
follow-up sessions.

## 90-second main pitch

**Opening frame (10 s)**

> RWA stablecoin settlements grew 8x in 2026. But banks still can't
> participate — every tokenization platform is stuck on compliance.
>
> AttestRWA fixes that. We turn bank verification rules into machine-
> verifiable on-chain attestations. Banks sign, escrows enforce, money
> moves only when the deal is bank-grade.

**Live action — happy path (25 s)**

> *(Wallet connects to Base Sepolia)*
> Buyer sends 500K Mock USDC to our `SettlementEscrow` contract.
>
> *(Attester service log streams in real time)*
> Our attester service detects the pending deal. It checks the payee
> against the developer feed — match. Runs wallet taint analysis — green.
> RAG retrieves the relevant compliance policy. Decision: approve.
>
> *(EAS attestation appears on Base Sepolia)*
> The attester signs an EAS `SettlementApproval` attestation on-chain.
> The escrow reads it, verifies, and releases USDC to the verified payee.
>
> *(BaseScan link visible)*
> Closing Passport hash visible on BaseScan. End-to-end compliant
> settlement in 12 seconds.

**Live action — reject path (20 s)**

> *(Reset wallet → new deal)*
> Same flow, but this time the payment instruction came from an agent
> claiming a different legal entity — `SRL Holding 2026`. Our developer
> feed says the authorized payee is `Siam Riverside Living`.
>
> *(Attester decision: REJECT)*
> Payee mismatch. The attestation is signed but with `payeeVerified =
> false`. The escrow refuses the release.
>
> *(Buyer refund tx visible)*
> The buyer can refund. Audit trail: full on-chain.

**Close (15 s)**

> One attestation schema. Any RWA. Any bank.
>
> We don't compete with Centrifuge or RealT. We're the compliance layer
> they plug into.
>
> Stablecoins meet compliance — without trusting either side.

**Roadmap (15 s)**

> Today on Base Sepolia testnet. Q3: first exchange pilot. Q4: first bank
> attester pilot. 2027: multi-jurisdiction across ASEAN.
>
> Open Apache-2.0. Public EAS schema. Public attester address. Composable
> from day one.

## 3-minute extended version

Use after the 90-second hook lands. Adds Pivot story, technical depth,
and Q&A bridges.

**Pivot story (40 s)**

> We started this project as B2B bank-grade settlement infrastructure for
> Thailand property — Closing Passport, payee verification, multi-channel
> consult. Before SEABW 2026 we ran a brutal market check.
>
> What we saw: bank compliance dashboards are a saturated category. The
> growth in 2026 is RWA stablecoin settlements. And our strongest
> primitives — payee mismatch detection, capital classification, evidence
> attestation — were already pointing toward an on-chain layer.
>
> So we pivoted. From B2B SaaS to a web3-native attestation primitive.
> Same engineering foundation, sharper edge, broader market. The AttestRWA
> stack shipped in roughly four hours of AI-assisted development. The
> previous generation is preserved in `archive/v0.5/` for transparency.

**Technical depth (50 s)**

> Stack: Foundry contracts with fuzz tests and slither audit. FastAPI
> attester service with RAG-grounded evidence pack via BGE-M3 embeddings
> and reranker on Qdrant. Single-screen Next.js wallet UI. Local dev runs
> on an Anvil fork of Base Sepolia, so the EAS protocol bytecode at the
> canonical addresses is the real production code — no mocked
> primitives.
>
> Our SettlementApproval schema has ten fields: dealId, attester address,
> payee address, token address, amount, capital class, evidence hash,
> jurisdiction, expiration, payee verification flag. The escrow contract
> hard-pins this schema UID — schema impostors revert at the require.
>
> Attestations are revocable. If an attester signs by mistake, they can
> revoke; the escrow re-checks at release time.

**Differentiator pass (25 s)**

> What we are not: not a tokenization platform, not a KYC provider, not a
> new chain, not our own stablecoin. Each of those is a saturated category
> with strong incumbents. We are the missing primitive between them.
>
> Pitch line: "We don't tokenize property. We tokenize the fact that a
> bank verified the deal."

**Distribution and on-chain visibility (15 s)**

> Two distribution channels live: Dune Analytics public dashboard for
> on-chain metrics — attestations per day, rejections by reason, top
> attesters — and a Farcaster Frame so any user can verify a settlement
> status from their feed.

**Close + ask (10 s)**

> Hackathon-stage MVP, fully open-source. Looking for: design partner bank
> for the first attester pilot. Looking for: stablecoin RWA platform to
> integrate as the first consumer. Talk to us.

## Backup video script (60 s, recorded against dev chain)

Use this when the live demo network is unreliable. Same 90-second arc but
narrated over screen recording. Show:

1. `./scripts/dev-chain.sh` running.
2. `cast send` posting the EAS attestation (terminal).
3. The local Next.js screen with the wallet connect + escrow release.
4. `getSchema(uid)` readback showing the canonical 10-field schema.
5. Final hold on the Closing Passport hash with BaseScan-style URL pattern
   (even if it's the local block explorer view, the hash format is
   identical to real testnet).

Cut at 60 seconds exactly. No music. Voiceover only.

## Q&A bridges (anticipated jury questions)

| Question | Bridge |
|----------|--------|
| Why EAS and not your own framework? | EAS is production, on Base + Optimism + Arbitrum + Linea + Scroll + zkSync. Reinventing it would dilute composability. |
| Why not just a smart contract that does the verification itself? | Off-chain compliance pulls in RAG, policy docs, jurisdiction-specific rules — too heavy for on-chain. Attester abstraction lets banks own the verification policy without rewriting Solidity. |
| What's the attester's incentive? | Fee per attestation paid by the deal counterparty or the RWA platform. Banks already monetize compliance review; we just give them an on-chain output format. |
| What about compromised attester keys? | Revocation via EAS. Escrow re-checks at release. Production attester keys go in HSMs; the demo uses an Anvil test key for clarity. |
| How is this different from Quantexa / Actimize? | Those are internal compliance dashboards. We expose a public, composable, on-chain primitive that any chain consumer (escrow, exchange, RWA platform) can verify. |
| What chains do you support? | EAS lives on Base, Optimism, Arbitrum, Linea, Scroll, zkSync. We deploy on Base Sepolia for the hackathon; mainnet rollouts are a config change. |
| Real or testnet for the demo? | Today on Base Sepolia local fork. Real testnet deploy in Week 3 of the pivot. Mainnet deferred until first pilot bank signs as an attester. |

## Logistics

- **Printable 1-pager:** [`PITCH_CHEATSHEET.md`](PITCH_CHEATSHEET.md) —
  stage speech, elevator pitch, Q&A, links (phone or A4).
- Live demo screen: `/` on the deployed Vercel URL (Week 3). For
  hackathon-day, ensure a hard-wired ethernet connection where possible.
- Backup video: ready on local laptop + cloud (Google Drive, Vercel asset).
- Pre-funded deals: 3 transactions already deposited into escrow before the
  demo starts so the live flow is just `release()` (zero faucet risk).
- Recording: phone on tripod at the laptop angle as triple backup.

## What we explicitly do not show

- The 53-doc legacy structure of v0.5.
- The buyer consult bot.
- Yield OS post-closing vision.
- Any Thai-specific legal advice screen.
- Production mainnet contracts (we are testnet-only at hackathon time).
