# AttestRWA — Pitch Cheatsheet (1 page)

**Print:** A4 or Letter, narrow margins, ~10–11 pt. Keep on phone or print for stage / hallway.

| | |
|---|---|
| **Project** | AttestRWA — Settlement Attestation Layer for RWA |
| **Author** | Aleksandr Mordvinov · [github.com/FUYOH666](https://github.com/FUYOH666) |
| **Repo** | [github.com/FUYOH666/attestrwa](https://github.com/FUYOH666/attestrwa) |
| **Demo video** | [youtube.com/shorts/BipB2qPzZz0](https://youtube.com/shorts/BipB2qPzZz0) (85 s, English subtitles) |
| **Hackathon** | [SEA Blockchain Week 2026](https://www.seablockchainweek.org/hackathon) |
| **License** | Apache-2.0 · Base Sepolia · EAS `SettlementApproval` schema |

---

## Killer line (memorize)

> **We don't tokenize property. We tokenize the fact that a bank verified the deal.**

---

## Stage speech (~75 s, English)

> Hi, I'm Aleksandr. This is **AttestRWA**.
>
> RWA stablecoin settlements grew 8x in 2026. Tokenization is solved — Centrifuge, RealT, Ondo already do that. **Compliance is not.** Banks still can't participate as first-class actors on-chain.
>
> AttestRWA is the missing layer. We turn bank verification rules into machine-verifiable **EAS attestations** on Base. A buyer deposits stablecoin into a programmable escrow. Our attester checks payee identity, capital classification, and compliance evidence — then signs an on-chain **SettlementApproval**. The escrow releases funds **only** when the attestation is valid.
>
> In our demo you see both paths: **approve** — money goes to the verified payee. **Reject** — payee mismatch, escrow refuses release, buyer gets a refund. Full audit trail on-chain.
>
> We don't tokenize property. We tokenize the fact that a bank verified the deal. One public schema. Any RWA platform can plug in. Any bank can become an attester.
>
> Open source, Apache 2.0, Slither-clean contracts, reproducible demo with one command. Thank you.

*Pause after the killer line. If nervous, start with the problem, not the stack.*

---

## Elevator pitch (15 s)

> AttestRWA is the compliance bridge for RWA stablecoin settlements. Banks sign EAS attestations; escrows enforce them. We don't compete with tokenization platforms — **we're the layer they plug into.**

## Hallway pitch (30 s)

> **Problem:** Everyone tokenizes assets, but no bank can say on-chain "this deal is bank-grade."
>
> **Solution:** Public EAS schema + escrow that releases USDC only on a valid attestation. Off-chain attester checks payee, capital class, evidence — on-chain only the result.
>
> **Edge:** Not tokenization, not KYC, not a new chain. A **composable primitive** Centrifuge / RealT read without forking us.

## Russian backup (20 s)

> AttestRWA — слой между RWA-платформами и банками. Платформы токенизируют актив, мы даём on-chain доказательство bank-grade проверки. Escrow отпускает стейблкоин только при валидной EAS-аттестации. Open source, Base, подключается без форка.

---

## What we built (scan before Q&A)

| # | Unique | One line |
|---|--------|----------|
| 1 | Positioning | Compliance **primitive**, not another RWA token |
| 2 | On-chain enforce | Escrow **hard-checks** EAS attestation — not a dashboard |
| 3 | Public schema | 10-field `SettlementApproval` — any contract can verify |
| 4 | Bank-as-attester | Bank earns fee per attestation; owns policy via YAML DSL |
| 5 | Two demo paths | Happy release + reject (payee mismatch) + buyer refund |
| 6 | RAG = evidence | AI explains; **never** moves funds autonomously |
| 7 | Engineering | Foundry 33/33 · pytest 62/62 · Slither 0 · CI green |
| 8 | Repro demo | `./scripts/demo-mode.sh` — real EAS bytecode, no faucet |
| 9 | Composable | Centrifuge / Maple / RealT = **customers**, not competitors |

---

## Q&A — short answers

| Question | Answer |
|----------|--------|
| Why EAS? | Production on Base, Optimism, Arbitrum. We add a schema, not new infra. |
| Why off-chain attester? | RAG, policies, jurisdiction — too heavy on-chain. Attester signs; escrow enforces. |
| Bank incentive? | Fee per attestation — same as compliance review, machine-readable output. |
| Compromised attester key? | EAS revocation; escrow re-checks at release. Prod keys in HSM. |
| vs Centrifuge / RealT? | They tokenize assets. We answer: *safe to send stablecoin to this payee?* |
| vs Quantexa / Actimize? | Internal dashboards. We expose a **public on-chain primitive** any consumer verifies. |
| Mainnet? | Hackathon MVP on Base Sepolia fork. Real testnet = config change; mainnet after first bank pilot. |
| Open source? | Yes — schema, contracts, attester service, Apache 2.0. |
| Demo without faucet? | Anvil fork of Base Sepolia — canonical EAS bytecode at `0x4200…0021`. |

---

## Links to show (QR or copy-paste)

```
Demo:     https://youtube.com/shorts/BipB2qPzZz0
GitHub:   https://github.com/FUYOH666/attestrwa
Schema:   docs/ATTESTATION_SCHEMA.md  (UID 0x1f64ec96…cc96)
One-liner: RWA's bottleneck is compliance. We're the layer platforms plug into.
Ask:      Design-partner bank or RWA platform for first integration pilot.
```

---

## Stage tips

1. Speak **slower** than feels natural; pause after killer line.
2. Don't apologize for local fork — it's a **feature** (real EAS, zero deps).
3. End with ask: *design-partner bank or RWA platform*.
4. Backup: play YouTube demo if live network fails.
