# Validation Report

> Updated 2026-05-20 — reflects **v0.5.13** (full project audit, Tier A doc sync). Full audit: [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md).

## Fresh Verification

Run date: 2026-05-20

Commands:

```bash
cd apps/api && uv run pytest -q
cd apps/web && pnpm run build
cd apps/api && CONSULT_RETRIEVAL_MODE=keyword uv run python ../../scripts/run_consult_dialogue_matrix.py --offline
uv run python scripts/run_scenario_matrix.py --api-url http://localhost:8080
./scripts/docker-smoke.sh   # when Docker stack up
curl http://localhost:8080/api/consult/contour/healthz
curl -X POST "http://localhost:8080/api/rag/ingest?dry_run=true"
```

Results:

- Backend: **64 tests passed** (incl. consult, contour, retrieval, dialogue matrix).
- Consult dialogue matrix (offline): **17/17 turns**, 9 scripts — [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md).
- Scenario matrix: **8/8** — [`SCENARIO_SIMULATION_REPORT.md`](SCENARIO_SIMULATION_REPORT.md).
- Frontend: Next.js production build passed.
- API version: **0.5.13** (`config.py`, `.env.example`).
- Buyer Consultation: live via FastAPI, web panel, WhatsApp bridge; USDT/cash purchase pitch; explicit fallback modes.
- RAG ingest (dry-run): **46 documents** (39 synthetic + 7 consult_kb).
- Consult contour: `all_ready: true` when Qdrant + BGE + LM Studio up.

## Demo Flow Walkthrough

| UI step | Status | Notes |
|---------|--------|-------|
| Pitch Screen | OK | Static thesis; outcomes not API-driven (P1 gap) |
| Supplier Contrast | OK | Live `/api/demo/supplier-contrast` |
| Developer Knowledge Hub | OK | Live API; WhatsApp/web channels `live` in payload |
| Settlement Flow panel | OK | Single `/api/demo/closing-passport` fetch |
| Yield Plan | OK | Vision stub |
| Guided Simulation | OK | Linear 6-step |
| Scenario Simulator | OK | 8 scenarios; RAG trace or explicit fallback |
| Buyer Consultation | **Live** | Web + API + WhatsApp; 4-turn jury arc |
| Settlement Branch Explorer UI | **Roadmap** | `NONLINEAR_DECISION_GRAPH.md` |

## Consult verification

```bash
curl -s -X POST http://localhost:8080/api/consult/message \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"validation","message":"а как покупать? у меня usdt","channel":"whatsapp"}' | jq '{intent, retrieval_mode, tools_used}'
```

Expected: `intent: mixed`; `scenario_hint:usdt-mixed-route` in tools; no prompt leak in reply.

## Product Fit Check

- **Primary customer:** banking anchor and regulated structures.
- **Consult = distribution** — same brain on WhatsApp and web.
- **Developer Knowledge Hub** — upstream SSOT vs agent payee.
- **LangGraph.js** documented; FastAPI consult is live MVP.
- **Web3:** metadata-only evidence attestation.

## Scenario Matrix (8 scenarios)

| Scenario | Capital | Bank action | Passport |
|----------|---------|-------------|----------|
| swift-clean-route | green | approve | generated |
| usdt-mixed-route | amber | conditional_approve | generated |
| mixed-capital-route | mixed | conditional_approve | varies |
| cash-red-route | red | reject/escalate | not_generated |
| developer-suspicious-route | green | escalate | after correction |
| agent-risk-route | varies | escalate | varies |
| prelaunch-off-platform-route | green | escalate/reject | not_generated |
| tier-one-landmark-route | green | approve | generated |

## Verdict

Ready for hackathon demo. Consult contour + dialogue matrix green. See [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) for P0/P1/P2 backlog.

## Related

- [`FINAL_STATUS_AND_NEXT_ACTIONS.md`](FINAL_STATUS_AND_NEXT_ACTIONS.md)
- [`HANDOFF.md`](HANDOFF.md)
- [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md)
