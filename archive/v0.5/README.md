# Archive — v0.5.x (Bankable Property Network)

> **Status:** Historical context. Not maintained. Kept in repo as evidence of
> the engineering foundation that preceded the AttestRWA pivot.

This directory will receive (during Week 1 of the pivot, via `git mv` to
preserve commit history):

- `apps/api/src/app/services/buyer_consultation.py` and related tests
- `services/whatsapp-bridge/` (Go whatsmeow bridge)
- `data/consult_knowledge/realestate-demo/` (Landmark Sukhumvit KB)
- `data/consult_dialogues/` (17-turn regression matrix)
- `apps/web/src/app/buyer-consultation-panel.tsx`
- `apps/web/src/app/post-closing-yield-plan.tsx`
- `apps/web/src/app/scenario-simulator.tsx`
- `apps/web/src/app/guided-deal-simulation.tsx`
- `apps/web/src/app/supplier-contrast-demo.tsx`
- `apps/web/src/app/developer-knowledge-hub.tsx`
- `apps/web/src/app/pitch-screen.tsx`
- ~45 of 53 docs from `docs/` (HANDOFF, AGENT_*, JOURNEY_*, STAKEHOLDER_*, etc.)

## What we kept (now repurposed)

| Asset | New role in v1 (AttestRWA) |
|-------|----------------------------|
| Payee mismatch detection (`siam-riverside-feed.json` vs agent payee) | Central demo moment — triggers on-chain attestation rejection |
| Capital classification (green/amber/red) | Extended to stablecoin wallet taint analysis (mock Chainalysis signals) |
| RAG (Qdrant + BGE + reranker) | Repurposed as "compliance evidence engine" — helps attester, does not decide |
| Closing Passport data model | Becomes EAS `SettlementApproval` attestation schema |
| Synthetic dataset | Extended with mock wallet addresses (buyer / escrow / developer treasury) |
| FastAPI + Next.js + Pydantic + uv discipline | Foundation. Tests remain. |
| Explicit fallback culture | Preserved — banks value it |

## Why we pivoted

See [`../../README.md`](../../README.md) — section "Why we pivoted (Pivot story)".

In short: the original Bankable Property Network was bank-grade B2B
settlement infrastructure for Thailand property. Before SEABW 2026 we ran a
market check and identified that:

1. Bank compliance dashboards are a saturated category (SAS, Quantexa, Actimize).
2. Real growth in 2026 is in RWA stablecoin settlements — and that market
   has no programmable compliance bridge.
3. Our strongest primitives (payee mismatch detection, capital
   classification, evidence attestation) were already pointing toward an
   on-chain layer.

So we pivoted to **AttestRWA — Settlement Attestation Layer for RWA**.
Same engineering foundation, sharper edge, broader market.

## Audit trail

| Tag | What it represents |
|-----|--------------------|
| `v0.5.13` | Last commit on `main` before pivot — full Bankable Property Network feature set |
| `v1.0.0` (target) | First AttestRWA release — RWA attestation layer on Base Sepolia |

To explore the previous generation, check out `main@v0.5.13`:

```bash
git checkout v0.5.13   # if tagged; otherwise: git checkout 7148ac5
```
