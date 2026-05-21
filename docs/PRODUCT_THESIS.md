# Product Thesis — AttestRWA

## One sentence

> AttestRWA is the on-chain compliance bridge that turns bank verification
> rules into machine-verifiable EAS attestations, so stablecoin settlements
> for real-world assets release only when the deal is bank-grade.

## The problem (2026)

Two facts about the RWA market in 2026:

1. **Stablecoin settlement volume is growing 8x year-over-year.** Cross-border
   property, private credit, trade-finance, and supply-chain payments are
   shifting to USDC and USDT rails because banks are too slow and expensive.
2. **Tokenization is a solved problem; compliance is not.** Centrifuge,
   Maple, RealT, Polytrade, Ondo — there is no shortage of tokenization
   platforms. None of them give a regulated bank a clean way to participate
   as an _attester_ on the same chain.

The result: trillions in stablecoin RWA flow with no programmable hook for
bank-grade verification. Buyers wire stablecoins to unverified payees.
Regulators have no audit trail. Markets get rug pulls. Banks stay locked
out of the fee opportunity.

## The solution

A minimal, composable primitive:

1. **`SettlementApproval` EAS schema** — a standardized on-chain attestation
   format with 10 fields covering deal identity, payee verification,
   capital classification, and evidence hash.
2. **`SettlementEscrow.sol`** — a programmable escrow contract that holds
   stablecoin deposits and releases them **only** when a valid attestation
   from a trusted attester is on-chain.
3. **Attester service (off-chain)** — applies bank-grade verification
   rules: payee must match upstream developer feed, capital classification
   must not be red, evidence pack must be RAG-grounded. Signs the EAS
   attestation. Never touches funds directly.
4. **Compliance-as-Code DSL** — a YAML rule language so an attester (a
   bank, a regulator, a custodian) declares its policy explicitly. Rules
   compile to attestation requirements that the escrow contract enforces.

## What makes this _the_ layer

| Other RWA projects | AttestRWA |
|--------------------|-----------|
| Tokenize property titles → legal mess | Attest settlement evidence → no ownership claims |
| Build new KYC providers (Sumsub, Persona class) | Integrate existing KYC; surface only the relevant signals on-chain |
| Run private permissioned chains | Public composable schema on EAS — any consumer can verify |
| Hardcode a single bank | Multi-attester registry — any regulated structure can become an issuer |
| Black-box AI compliance | RAG-assisted, schema-bound, explainable; AI never autonomously moves funds |

## Primary customers

1. **Banks and regulated structures** — earn a fee per attestation; grow
   high-margin custody / FET / escrow business; on-board affluent foreign
   clients through compliant rails. Banks remain the ultimate authority on
   whether money moves; we just give them a machine-readable signal layer.
2. **Stablecoin RWA platforms** (Centrifuge, Maple, RealT class) — plug in
   AttestRWA as the compliance layer they currently lack. We do not compete
   with their tokenization; we make their settlement bank-compatible.
3. **Exchanges entering RWA** (Binance Settlement, OKX RWA, Bybit RWA) —
   use AttestRWA attestations as the gating signal for their RWA product
   listings.

Buyer protection (no wires to fraudulent payees) is the **social bonus**, not
the product target.

## Why now (2026)

- Stablecoin settlement is no longer niche — it is the default rail for
  cross-border RWA in 2026.
- EAS is mature; it has shipped on Base, Optimism, Arbitrum, Linea, Scroll,
  zkSync. We do not have to invent the attestation primitive.
- Major banks (DBS, SCB, HSBC, Standard Chartered) all have stablecoin /
  RWA programs but no shared standard for on-chain compliance signalling.
- Regulators (MAS, BoT, SFC) are moving toward "permissioned DeFi" — they
  need a machine-readable evidence trail, not opaque off-chain dashboards.

## Why not us building yet another tokenization platform

We deliberately do not build tokenization, lending, or yield products. Two
reasons:

1. **Saturated.** Centrifuge ($800M+ TVL), Maple ($2B+), Ondo Finance ($10B+)
   already serve those niches well.
2. **Wrong layer.** All of them are stuck on compliance. We solve their
   shared bottleneck, not their differentiated product surface.

## Social impact (the bonus, not the pitch)

RWA platforms today let anyone tokenize anything. AttestRWA adds the missing
verifier: developer authenticity, payee authority, capital cleanliness.
Buyers no longer wire stablecoins to unverified payees. Regulators get
audit-grade on-chain evidence. Markets get fewer rug pulls. **This is RWA
growing up.**

## Non-goals (explicit)

- We do not tokenize property titles or any real asset.
- We do not issue our own stablecoin.
- We do not run our own KYC.
- We do not run our own L1 / L2.
- AI does not autonomously approve money movement; it helps regulated
  structures review evidence faster.
- We do not claim production-grade Sansiri / SCB / Bangkok Bank /
  Standard Chartered partnerships at hackathon time. Pilot conversations
  are roadmap-only.

## Pivot context

This product is the v1.0 of a project that began as Bankable Property
Network — a B2B bank settlement infrastructure focused on Thailand
property. The pivot was deliberate and shipped for SEABW 2026 in roughly
four hours of AI-assisted development: same engineering foundation (payee
verification, capital classification, RAG evidence engine, FastAPI +
Next.js base), sharper edge (on-chain), broader market (RWA, not just
Thailand property).

The previous generation lives in [`archive/v0.5/`](../archive/v0.5/) for
auditability — see `archive/v0.5/README.md` for what was archived and why.
