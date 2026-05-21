# Project Description — AttestRWA

```yaml
audience: hackathon_registration_reviewers
language: en
project: AttestRWA
version: 1.0.0
author: Aleksandr Mordvinov
author_url: https://github.com/FUYOH666
data: synthetic_demo_only
primary_customer: banks_and_regulated_structures
hackathon: SEA Blockchain Week 2026
```

> **Use for hackathon registration and "Project Description" uploads.**
> English, stable narrative — safe to copy-paste into platform forms.
> Export to PDF if the form requires a file upload (Markdown → Print → PDF).

---

## Project Name

**AttestRWA**

## Tagline

Settlement Attestation Layer for RWA — on-chain compliance bridge that turns bank verification rules into machine-verifiable EAS attestations, so stablecoin payments for real-world assets release only when the deal is bank-grade.

**Pitch line:** We do not tokenize property. We tokenize the fact that a bank verified the deal.

---

## Problem

Two facts about the RWA market in 2026:

1. **Stablecoin settlement volume is growing 8x year-over-year.** Cross-border property, private credit, trade-finance, and supply-chain payments are shifting to USDC and USDT rails because banks are too slow and expensive.
2. **Tokenization is a solved problem; compliance is not.** Centrifuge, Maple, RealT, Polytrade, Ondo — there is no shortage of tokenization platforms. None of them give a regulated bank a clean way to participate as an _attester_ on the same chain.

The result: trillions in stablecoin RWA flow with no programmable hook for bank-grade verification. Buyers wire stablecoins to unverified payees. Regulators have no audit trail. Banks stay locked out of the fee opportunity.

---

## Solution

AttestRWA is a minimal, composable compliance primitive — not another tokenization platform:

1. **`SettlementApproval` EAS schema** — standardized on-chain attestation (10 fields: deal identity, payee verification, capital classification, evidence hash, jurisdiction, expiration).
2. **`SettlementEscrow.sol`** — programmable escrow that holds stablecoin and releases funds **only** when a valid attestation from a trusted attester is on-chain.
3. **Attester service (FastAPI)** — applies bank-grade rules: payee must match upstream developer feed, capital must not be red, evidence must be RAG-grounded. Signs the EAS attestation. Never touches funds directly.
4. **Compliance-as-Code DSL** — YAML policy language so any bank, regulator, or custodian declares its verification rules explicitly.

We do **not** compete with Centrifuge or RealT. We are the compliance layer they plug into.

---

## Who Benefits

| Stakeholder | Value |
|-------------|--------|
| **Banks / regulated structures** | Fee per attestation; machine-readable on-chain output; grow custody / escrow / FET business |
| **RWA tokenization platforms** | Bank-compatible settlement without building compliance in-house |
| **Exchanges entering RWA** | Gating signal for listings — read public EAS schema, no fork required |
| **Regulators** | Audit-grade on-chain evidence trail, not opaque dashboards |
| **Buyers (social bonus)** | Escrow refuses release to unverified payees; refund path on reject |

---

## What We Demonstrate (Hackathon MVP)

Reproducible demo in one command (`./scripts/demo-mode.sh`):

1. **Happy path** — buyer deposits Mock USDC → attester approves → EAS attestation on-chain → escrow releases to verified payee.
2. **Reject path** — payee mismatch (`SRL Holding 2026` vs authorized `Siam Riverside Living`) → attestation signed with `payeeVerified = false` → escrow refuses release → buyer refunds.
3. **Real EAS bytecode** — Anvil fork of Base Sepolia; canonical EAS contract at `0x4200…0021` (no mocked primitives).
4. **85-second demo video** — terminal + on-chain proof, English subtitles.
5. **Optional UI** — single-screen Next.js wallet flow (`/rwa-settlement-live`).
6. **Farcaster Frame** — verify settlement status from feed (`/api/frame/attest`).

**Engineering quality:** Foundry 33/33 tests, pytest 62/62, Slither 0 findings, CI green.

---

## Technology Overview

| Layer | Stack |
|-------|--------|
| Contracts | Solidity 0.8.26, Foundry (forge / anvil / cast), Base Sepolia |
| Attestations | Ethereum Attestation Service (EAS), public `SettlementApproval` schema |
| API | Python 3.12+, FastAPI, uv |
| Web | Next.js, TypeScript, pnpm, wagmi + viem + RainbowKit |
| Compliance engine | YAML DSL, wallet taint classifier, RAG evidence (Qdrant + BGE) |
| Dev simulation | Anvil fork of Base Sepolia — no external faucet required for demo |

AI does **not** decide whether money moves. AI helps regulated structures review evidence faster, with traceability.

---

## Data and Ethics

- All demo data is **synthetic** — no real passports, bank statements, wallets, or contracts.
- Fictional developers and projects — **not** real developer or bank endorsements.
- Bank names (SCB, DBS, HSBC, etc.) appear as market examples only; no implied partnership unless explicitly agreed offline.
- No tokens issued. No mainnet deploy at hackathon time. Apache-2.0 open source.

---

## Links

| Field | Value |
|-------|--------|
| Author | [Aleksandr Mordvinov](https://github.com/FUYOH666) |
| Repository | https://github.com/FUYOH666/bankable-property-network |
| Demo video | https://youtube.com/shorts/BipB2qPzZz0 |
| Pitch deck (PDF) | [`AttestRWA-PITCH-DECK.pdf`](AttestRWA-PITCH-DECK.pdf) |
| Landing page | https://scanovich.ai/seablockchainweek/ |
| Hackathon | https://www.seablockchainweek.org/hackathon |
| License | Apache-2.0 |

---

## Copy-Paste Blocks (Registration Forms)

### Short description (~280 characters)

AttestRWA is the Settlement Attestation Layer for RWA. We turn bank verification rules into machine-verifiable EAS attestations on Base. Programmable escrow releases stablecoin only when the deal is bank-grade. We don't tokenize assets — we're the compliance layer platforms plug into. Open source.

### Medium description (~600 characters)

RWA stablecoin settlements grew 8x in 2026, but banks still can't participate on-chain — tokenization is solved, compliance is not. AttestRWA fixes that with a public EAS SettlementApproval schema, a programmable SettlementEscrow contract, and a FastAPI attester service that checks payee identity, capital classification, and RAG-grounded evidence before signing on-chain. Demo shows both approve and reject paths with full audit trail. We don't compete with Centrifuge or RealT; we're the composable primitive they integrate. Foundry + pytest + Slither-clean. Apache-2.0.

### Problem (one paragraph)

Stablecoin RWA settlement volume is growing rapidly, but regulated banks have no standard way to signal "this deal is bank-grade" on-chain. Tokenization platforms handle asset representation; none provide a public, composable compliance bridge that escrows enforce. Buyers wire USDC to unverified payees. Regulators lack machine-readable audit trails. Banks miss the attestation fee opportunity.

### Solution (one paragraph)

AttestRWA converts bank verification rules into EAS attestations that any escrow, exchange, or RWA platform can verify without forking our code. A buyer deposits stablecoin into SettlementEscrow; our attester checks payee authority, capital class, and evidence; the escrow releases funds only on a valid attestation. One public schema. Any RWA. Any bank as attester.

### Impact (one paragraph)

Banks earn fees per attestation with on-chain audit output. RWA platforms become bank-compatible without building compliance in-house. Regulators get transparent evidence trails. Buyers benefit indirectly — escrow blocks releases to fraudulent payees and enables refunds on reject. The layer scales across jurisdictions via attester policy, not protocol rewrites.

### Team / author (registration form)

Aleksandr Mordvinov — https://github.com/FUYOH666

### Demo URL (registration form)

https://youtube.com/shorts/BipB2qPzZz0

### GitHub URL (registration form)

https://github.com/FUYOH666/bankable-property-network

---

## Related Docs

- [`PRODUCT_THESIS.md`](PRODUCT_THESIS.md) — problem, solution, positioning
- [`COMPARISON.md`](COMPARISON.md) — vs Centrifuge, Maple, RealT, Ondo
- [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) — 90-second pitch script
- [`PITCH_CHEATSHEET.md`](PITCH_CHEATSHEET.md) — printable stage / hallway cheat sheet
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — technical architecture
- [`ATTESTATION_SCHEMA.md`](ATTESTATION_SCHEMA.md) — EAS schema specification

## Pivot Context

This project began as Bankable Property Network (B2B bank settlement for Thailand property). We pivoted to AttestRWA for SEABW 2026 and shipped the full stack in roughly four hours of AI-assisted development. Previous generation preserved in [`archive/v0.5/`](../archive/v0.5/) for auditability.
