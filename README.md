# AttestRWA

> **Settlement Attestation Layer for RWA** — on-chain compliance bridge that
> turns bank verification rules into machine-verifiable attestations, so
> stablecoin payments for real-world assets release only when the deal is
> bank-grade.

[![Status](https://img.shields.io/badge/status-v1.0.0--rc-orange)](#)
[![Network](https://img.shields.io/badge/network-Base%20Sepolia-blue)](https://sepolia.basescan.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Hackathon](https://img.shields.io/badge/hackathon-SEA%20Blockchain%20Week%202026-purple)](https://www.seablockchainweek.org/hackathon)

**Author:** [Aleksandr Mordvinov](https://github.com/FUYOH666) ·
**Repository:** [github.com/FUYOH666/bankable-property-network](https://github.com/FUYOH666/bankable-property-network) (rename to `attestrwa` post-pivot) ·
**Demo:** _to be set when v1.0.0 deploys_

---

## Hook (one sentence)

> RWA's bottleneck in 2026 is not tokenization — it's compliance.
> We don't compete with Centrifuge or RealT; we're the layer they plug into.

## What you see when you open the demo (90 seconds)

1. **Frame** (10 s): "RWA settlements grew 8x in 2026. Banks still can't participate."
2. **Buyer wallet** (15 s) sends 500K Mock USDC to `SettlementEscrow` on Base Sepolia.
3. **Attester** (FastAPI, 20 s) detects pending settlement, reads developer
   feed, runs Property Shield + RAG-assisted evidence, signs an EAS
   `SettlementApproval` attestation.
4. **Branch A (HAPPY)** — attestation valid → escrow releases USDC to verified
   payee → on-chain Closing Passport hash visible on BaseScan.
   **Branch B (REJECT)** — payee mismatch (`SRL Holding 2026` vs
   `Siam Riverside Living`) → attestation rejected → escrow refunds buyer →
   audit log on-chain.
5. **Story close** (15 s): "One attestation schema. Any RWA. Any bank.
   Stablecoins meet compliance — without trusting either side."

## What's on-chain

### Dev simulation (Anvil fork of Base Sepolia — port 8545, chain 84532)

Spin up the full stack in one command: `./scripts/dev-chain.sh`. See
[`docs/DEV_SIMULATION.md`](DEV_SIMULATION.md).

| Artefact | Address / UID |
|----------|---------------|
| `SettlementApproval` EAS Schema UID | `0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96` |
| EAS contract (canonical) | `0x4200000000000000000000000000000000000021` |
| SchemaRegistry (canonical) | `0x4200000000000000000000000000000000000020` |
| Attester EOA (dev) | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` (Anvil acc 0) |
| `SettlementEscrow.sol` | _(deploy Week 2)_ |
| `MockUSDC.sol` | _(deploy Week 2)_ |

### Real Base Sepolia (Week 3 — public for hackathon submission)

| Artefact | Status |
|----------|--------|
| Schema UID | Same as dev (deterministic) — to be registered Week 3 |
| Attester EOA (real, public address) | _(generate Week 3)_ |
| BaseScan deploy link | _(Week 3)_ |
| EAS Scan schema link | _(Week 3)_ |
| Dune dashboard | _(Week 3 — public)_ |
| Farcaster Frame | `/api/frame/attest` _(Week 3 — public)_ |

## Architecture (minimal)

```text
Buyer wallet  --USDC-->  SettlementEscrow.sol  --reads-->  EAS Registry
                              ^                                ^
                              | release/refund                 | write attestation
                              |                                |
                              +--------- Attester (FastAPI) ---+
                                              |
                                              v
                              Compliance Engine: Property Shield + RAG + Capital Map
                                              |
                                              v
                              Developer Feed (synthetic SSOT)
```

Full diagram: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) _(to be written Week 1)_

## Why we pivoted (Pivot story)

We started this project as a B2B bank-grade settlement infrastructure for
Thailand property — Closing Passport, payee verification, multi-channel
buyer consult. Six weeks in (commit history visible at `main@v0.5.13`), we
ran a brutal market check and saw that:

1. Bank compliance dashboards are already a saturated category (SAS,
   Quantexa, Actimize).
2. Real growth in 2026 is in RWA stablecoin settlements — and that market
   has no programmable compliance bridge.
3. Our strongest primitives (payee mismatch detection, capital
   classification, evidence attestation) were already pointing toward an
   on-chain layer.

So we pivoted from B2B SaaS to a web3-native attestation primitive:
**Settlement Attestation Layer for RWA**. Same engineering foundation,
sharper edge, broader market.

The pivot is in this repo — see [`archive/v0.5/`](archive/v0.5/) for the
previous generation. We kept what mattered (payee logic, capital
classification, RAG, FastAPI/Next.js base, 64 pytest baseline), killed what
didn't (buyer consult, WhatsApp bot, 8 panels, 45 docs).

## Why this wins at SEA Blockchain Week 2026

- **Most RWA projects** build tokenization (Centrifuge, Maple, RealT,
  Polytrade) — we don't compete, we're the layer above.
- **Most compliance projects** are KYC (Sumsub, Persona) — we're on-chain
  attestation primitives, not identity.
- **Most blockchain-property projects** tokenize titles — legal mess. We
  attest settlement evidence, not ownership claims.

**Pitch line:** "We don't tokenize property. We tokenize the fact that a
bank verified the deal."

## Social impact

RWA platforms today let anyone tokenize anything. AttestRWA adds the
missing verifier: developer authenticity, payee authority, capital
cleanliness. Buyers no longer wire stablecoins to unverified payees.
Regulators get audit-grade evidence. Markets get fewer rug pulls.
This is RWA growing up.

## Roadmap

| When | What |
|------|------|
| **Week 0 (now)** | Branch, archive scaffold, EAS schema registered, draft narrative |
| **Week 1** | Surgery: archive old modules, rebrand AttestRWA, slim docs to 8 files, synthetic data with wallet addresses, 3 RWA scenarios |
| **Week 2** | Foundry contracts + fuzz tests + slither clean + deploy to Base Sepolia; attester service + EAS client + DSL + wallet taint; single-screen UI with wagmi/viem |
| **Week 3** | Farcaster Frame, Dune dashboard, audit polish, 60s recorded video, README hero finalization, `v1.0.0` tag |
| **Q3 2026** | First exchange integration — Binance Settlement / OKX RWA / Bybit RWA pilot |
| **Q4 2026** | First bank attester pilot (Thailand or Singapore) — paid fee per attestation |
| **2027** | Multi-jurisdiction ASEAN expansion, L2 mainnet, compliance DSL marketplace |

## Tech stack

| Layer | Choice |
|-------|--------|
| L2 | Base Sepolia (testnet) → Base mainnet (production) |
| Attestations | EAS (Ethereum Attestation Service) |
| Stablecoin | Mock USDC ERC-20 (demo); USDC / USDT (production) |
| Contracts | Solidity 0.8.x + Foundry (fuzz + invariants + slither) |
| Wallet | wagmi + viem + RainbowKit |
| Backend | Python 3.12 + FastAPI + uv |
| Compliance evidence | Qdrant + BGE-M3 + reranker (RAG over synthetic policy corpus) |
| LLM (explainability only, optional) | LM Studio (Qwen-class) — schema-bound, never auto-decides |
| Frontend | Next.js + TypeScript + pnpm |
| Analytics | Dune Analytics (public dashboard) |
| Distribution | Farcaster Frame |

## What we don't build (explicit boundaries)

- We don't tokenize property (legal mess).
- We don't issue our own stablecoin.
- We don't do KYC (integrate Sumsub/Persona later).
- We don't run our own L1/L2.
- AI does not autonomously move money — it helps regulated structures
  review evidence faster, traceably, in a controlled environment.

## License

Apache-2.0. Schema, attester address, and contracts are public.

---

_This document is the **Week 0 draft** of the new root README. It replaces
the v0.5 README in Week 1 (when the old README moves to
`archive/v0.5/README.md`)._
