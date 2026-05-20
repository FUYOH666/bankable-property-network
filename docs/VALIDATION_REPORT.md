# Validation Report

> Updated 2026-05-20 — reflects **v0.5.5** (Developer Supply Demo: off-platform vs tier-1 contrast).

## Fresh Verification

Run date: 2026-05-20

Commands:

```bash
cd apps/api && uv run pytest -q
cd apps/web && pnpm run build
# API on :8080
curl http://localhost:8080/healthz
curl http://localhost:8080/api/demo/closing-passport
curl http://localhost:8080/api/demo/developer-knowledge-hub
curl http://localhost:8080/api/demo/supplier-contrast
curl http://localhost:8080/api/demo/guided-simulation
curl http://localhost:8080/api/demo/evidence-pack
curl http://localhost:8080/api/demo/post-closing-yield-plan
curl http://localhost:8080/api/scenarios
curl http://localhost:8080/api/scenarios/prelaunch-off-platform-route/run
curl http://localhost:8080/api/scenarios/tier-one-landmark-route/run
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run?mode=fallback"
curl http://localhost:8080/api/rag/health
```

Results:

- Backend: **37 tests passed** (+4 supplier contrast / new scenarios).
- Frontend: Next.js production build passed (includes `supplier-contrast-demo.tsx`).
- Smoke matrix: **12/12 endpoints HTTP 200** (added `supplier-contrast`, two new scenario runs).
- Supplier contrast: `off_platform.developer` = Shadow Bay; `on_network.feed_snapshot.permit_status` = `issued`.
- New scenarios: `prelaunch-off-platform-route` → `closing_passport_status=not_generated`; `tier-one-landmark-route` → `approve` + passport generated.
- Developer Knowledge Hub: `knowledge_vs_agent_gap.status` = `mismatch_detected`.
- RAG fallback: `retrieval_mode` = `deterministic_fallback` (explicit, no silent degrade).
- Scenarios: **8** returned from `GET /api/scenarios`.
- API version config aligned to **0.5.5** (`config.py`, `.env.example`).

## Demo Flow Walkthrough (expected gaps)

| UI step | Status | Notes |
|---------|--------|-------|
| Pitch Screen | OK | Static + thesis; **Why Developers Join** card |
| Supplier Contrast | OK | Live `/api/demo/supplier-contrast` |
| Developer Knowledge Hub | OK | Live API |
| Settlement Flow panel | OK | Single `/api/demo/closing-passport` fetch |
| Yield Plan | OK | Vision stub |
| Guided Simulation | OK | Linear 6-step (future LangGraph target) |
| Scenario Simulator | OK | 8 scenarios; RAG trace or fallback |
| Buyer Consultation Agent chat | **Not live** | Doc-only; `apps/buyer-agent/` not scaffolded |
| Settlement Branch Explorer UI | **Not live** | Documented in `NONLINEAR_DECISION_GRAPH.md` |

Presenter lines verified in docs: local AI contour + nonlinear decision graph (`HACKATHON_RUNBOOK.md`, `DEMO_CHECKLIST.md`).

## Product Fit Check

The MVP matches the money infrastructure thesis:

- **Primary customer:** banking anchor and regulated structures.
- **Bankable Property OS** is the operating layer; **Closing Passport** is the first module.
- **Developer Knowledge Hub** is upstream SSOT — agent payee vs developer feed.
- **Settlement Flow panel** shows live API data: Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport hash.
- **Agent architecture (0.5.4):** LangGraph.js primary; buyer consultation + settlement graph documented; code scaffold is next build.
- **Social bonus:** buyer avoids irreversible deposit to wrong entity when rails exist.
- **Web3:** metadata-only evidence attestation, not property ownership tokenization.

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

## Staff Review

Historical baseline: [`STAFF_REVIEW_0.5.4.md`](STAFF_REVIEW_0.5.4.md) (pre–0.5.5). **Current audit entry:** [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md).

**Verdict:** Ready for hackathon demo. No blockers. Next product build: `apps/buyer-agent/` LangGraph scaffold.

## Related

- Live status: `docs/FINAL_STATUS_AND_NEXT_ACTIONS.md`
- Agent handoff: `docs/HANDOFF.md`
- Presenter flow: `docs/DEMO_CHECKLIST.md`
