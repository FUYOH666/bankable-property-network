# AGENTS.md — AttestRWA

Settlement Attestation Layer for RWA. Web3-native on-chain compliance bridge
for cross-border stablecoin real-world-asset settlements. Hackathon target:
SEA Blockchain Week 2026.

**Branch:** `main` (merged from `v1/attestation-layer` at `v1.0.0`).
**Version:** `1.0.0` (SEA Blockchain Week 2026 hackathon submission).
**Build time:** ~4 hours AI-assisted development after pivot from v0.5 prototype.
**Predecessor:** Bankable Property Network (archive/v0.5/).

## Stack

| Layer | Tool |
|-------|------|
| Contracts | Solidity 0.8.x, **Foundry** (forge / cast / anvil / chisel 1.7.1) |
| L2 | **Base Sepolia** (chainId 84532); local fork via Anvil for development |
| Attestations | **EAS** at canonical `0x4200…0021` (SchemaRegistry `0x4200…0020`) |
| Stablecoin | Mock USDC ERC-20 (own deployment, week 2) |
| Wallet | wagmi + viem + RainbowKit (week 2) |
| API | Python 3.12+, **uv**, FastAPI |
| Frontend | Next.js, TypeScript, pnpm |
| RAG (compliance evidence) | Qdrant + BGE-M3 embedding + BGE reranker |
| LLM (explainability only) | LM Studio (Qwen-class), schema-bound, never autonomous |
| Analytics | Dune Analytics public dashboard (week 3) |
| Distribution | Farcaster Frame (week 3) |

## Commands

```bash
# Dev chain (Anvil fork of Base Sepolia + EAS schema registered)
./scripts/dev-chain.sh        # one-shot setup, idempotent
./scripts/stop-dev-chain.sh   # tear down

# API
cd apps/api && uv sync && uv run pytest -q
cd apps/api && uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080

# Web
cd apps/web && pnpm install && pnpm dev
cd apps/web && pnpm run build

# Contracts (Foundry workspace, Week 2 fills these in)
cd contracts && forge build && forge test -vvv --gas-report
cd contracts && slither .   # zero high/medium target

# Health
curl http://localhost:8080/healthz
```

## Demo flow (target Week 2)

Single screen (`/`), wallet connect, 90-second arc:

1. Buyer wallet sends Mock USDC to `SettlementEscrow` on Base Sepolia (dev fork in week 1, real testnet in week 3).
2. Attester service detects pending settlement, runs Property Shield + RAG compliance, signs EAS attestation.
3. Branch A (HAPPY) — attestation valid → escrow releases USDC to verified payee.
4. Branch B (REJECT) — payee mismatch / red capital / expired attestation → escrow refunds buyer.

## Key endpoints (current — Week 1)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/healthz` | Liveness |
| GET | `/api/demo/closing-passport` | Legacy settlement flow data (basis for attester logic) |
| GET | `/api/demo/developer-knowledge-hub` | Upstream developer feed (drives payee verification) |
| GET | `/api/demo/supplier-contrast` | Off-platform vs tier-1 supplier data |
| GET | `/api/demo/evidence-pack` | Evidence pack export (privacy-safe) |
| GET | `/api/scenarios` | Scenario list (to be replaced with 3 RWA scenarios in week 1.4) |
| GET | `/api/scenarios/{id}/run` | Run scenario |
| GET | `/api/scenarios/{id}/rag-run` | Run scenario with RAG trace |
| GET | `/api/rag/health` | RAG / compliance evidence engine health |
| POST | `/api/rag/ingest` | Ingest synthetic corpus into Qdrant |

Week 2 adds: `POST /attest/settlement`, `GET /attest/{dealId}`, `GET /attest/healthz`.

## Conventions

- Python: **uv only** (no pip), `logging` not `print`, `/healthz` required.
- Use `app.paths.synthetic_root()` + `app.services.data_loader.load_json`; never duplicate `Path(__file__).parents[N]`.
- Secrets in `.env`; dev attester key in `.env.example` is the well-known Anvil test key (public, never use on mainnet).
- After substantive changes: run `uv run pytest -q` (apps/api), `pnpm run build` (apps/web), and `forge test` (contracts, when present).

## Do not

- Commit secrets, real attester private keys, TailScale IPs, or internal hostnames.
- Edit files under `.cursor/plans/`.
- Use `pip install` without `uv`.
- Reintroduce buyer-consult / WhatsApp / Yield panels (they live in `archive/v0.5/` as historical context).
- Claim production WhatsApp / Telegram / Line / Meta Business API integration.
- Claim mainnet deploy or real RWA-platform partnerships (testnet only for hackathon).

## Pivot context (read before large changes)

- Read [`docs/DEV_SIMULATION.md`](docs/DEV_SIMULATION.md) — how to spin up the local dev chain.
- Read [`docs/ATTESTATION_SCHEMA.md`](docs/ATTESTATION_SCHEMA.md) — EAS schema and integration model.
- Read [`docs/PRODUCT_THESIS.md`](docs/PRODUCT_THESIS.md) — problem, solution, primary customers.
- Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — layers, data flow, design decisions.
- Read [`docs/ROADMAP.md`](docs/ROADMAP.md) — Week 0 → Week 3 → 2027.
- Read [`archive/v0.5/docs/WEEK0_BOOTSTRAP.md`](archive/v0.5/docs/WEEK0_BOOTSTRAP.md) — what was locked in Week 0 (historical).
- Read `.cursor/plans/godmode-pivot-attestation-layer_*.plan.md` — full plan.

## New chat starter

```text
Project: AttestRWA — Settlement Attestation Layer for RWA. Branch
v1/attestation-layer from main@v0.5.13. Read AGENTS.md, docs/PRODUCT_
THESIS.md, docs/ARCHITECTURE.md, docs/DEV_SIMULATION.md, docs/
ATTESTATION_SCHEMA.md first.
Network: Base Sepolia (chainId 84532), dev via Anvil fork on :8545.
Stack: contracts (Foundry, Week 2), apps/api (FastAPI, uv), apps/web
(Next.js, pnpm). Legacy v0.5 in archive/v0.5/. Do not edit .cursor/plans/.
```
