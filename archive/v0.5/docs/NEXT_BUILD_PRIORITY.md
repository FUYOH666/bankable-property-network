# Next Build Priority

> Updated 2026-05-20 — post [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) audit (v0.5.13).

## Completed (through 0.5.13)

1. MVP scorecard — [`EFFECTIVENESS_SCORECARD.md`](EFFECTIVENESS_SCORECARD.md) re-scored.
2. Guided Deal Simulation — live API + UI.
3. Synthetic simulation artifacts + Evidence Pack JSON export.
4. **RAG pipeline live** — Qdrant + BGE + reranker; 46-doc ingest; explicit fallback.
5. **Buyer Consultation live** — FastAPI + WhatsApp + web; Landmark KB; USDT/cash pitch; 17/17 dialogue matrix.
6. Supplier Contrast + Developer Knowledge Hub.
7. Full project audit + Tier A doc sync.

## P0 — Before booth / jury

1. `./scripts/docker-smoke.sh` + `GET /api/consult/contour/healthz` → `all_ready`.
2. Pre-record 60s backup capture.
3. Deploy API (+ static web) for scanovich.ai — [`DEPLOY.md`](DEPLOY.md), [`PUBLISH_SEABLOCKCHAINWEEK.md`](PUBLISH_SEABLOCKCHAINWEEK.md).

## P1 — Serious product polish

4. Consult panel: judge mode — `retrieval_mode`, citations, tools_used visible.
5. PitchScreen: partial API-driven outcomes from `/api/scenarios`.
6. Settlement panel: visual payee mismatch callouts.
7. Web optional Docker profile for one-command booth.
8. `scripts/audit-docs.sh` — version/test-count drift grep.

## P2 — Post-hackathon

9. LangGraph scaffold — `apps/buyer-agent/` — [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).
10. Settlement Branch Explorer UI — [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md).
11. PDF Closing Passport export.
12. Telegram adapter (thin wrapper on `POST /api/consult/message`).

## Do Not Prioritize Yet

- Real smart contract, KYC/KYB, title registry.
- Multi-case marketplace beyond demo scenarios.
- Full Thai legal PDF corpus as authoritative RAG.
- Property tokenization.
