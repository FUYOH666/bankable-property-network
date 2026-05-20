# Staff Review — v0.5.4 verification pass

> **Historical.** Scope covered through agent architecture docs (0.5.4). **v0.5.5** added Developer Supply Demo, `supplier-contrast` API/UI, 8 scenarios, and `docs/PROJECT_DESCRIPTION.md` + `docs/AI_AUDIT_INDEX.md`. Current counts: [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md). AI auditors: [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md).

**Date:** 2026-05-20  
**Mode:** full  
**Scope:** Doc-pass 0.5.3 (local AI contour) + 0.5.4 (agent architecture) + existing FastAPI/Next.js MVP. Excludes `node_modules/`, `.venv/`, `.next/`, plan files. No code review of vendored deps.

---

## Scope

**Goal:** Confirm hackathon demo readiness after documentation expansion for local AI tiers, nonlinear decision graph, and buyer consultation agent spec.

**Modules touched (docs):** `NONLINEAR_DECISION_GRAPH.md`, `BUYER_CONSULTATION_AGENT.md`, `AGENT_STACK_EVALUATION.md`, cross-links across 20+ docs; version alignment in `config.py`, `.env.example`.

**Modules unchanged (code):** `apps/api`, `apps/web` — no buyer-agent implementation (expected).

**Assumption:** Demo runs locally with API on `:8080`; RAG live mode optional; fallback mode acceptable for judges.

---

## Correctness and logic

- **Routing invariant:** `compare_settlement_routes()` always marks `bankable_escrow` as `recommended: True`; `pick_recommended_route()` falls back to `bankable_escrow` — covered by `test_routing.py` and `test_closing_passport.py`.
- **RAG fallback:** Explicit `deterministic_fallback` when services unavailable; smoke confirmed on `rag-run?mode=fallback`.
- **No LLM payment authority:** RAG retrieve path does not call LM Studio; docs state buyer agent does not approve settlement — consistent with bank-first thesis.
- **Developer hub anchor:** `mismatch_detected` on payee gap — smoke confirmed.

No logic regressions found in automated tests.

---

## Architecture fit

- **Two-layer model** clearly documented: Buyer Consultation Agent (discovery) vs Bankable Property OS (deterministic settlement graph).
- **LangGraph.js primary** — appropriate for bank-grade branching, human gates, audit; Mastra secondary; OpenClaw/Hermes rejected as core — sound for regulated context.
- **Local contour** separated from enterprise tier (LM Studio/vLLM, BGE/Qwen) — no hidden fallbacks in docs.
- **Gap (expected):** Documented graph nodes map to existing API modules, but LangGraph runtime not wired — acceptable for doc-first phase.

---

## Security and privacy

- Grep/docs review: no TailScale IPs or secrets in committed `.env.example` or public docs (placeholders only).
- Evidence pack excludes sensitive fields — tested in `test_closing_passport.py`.
- Buyer agent spec restricts tools to HTTP API (no shell/browser) — correct trust model.
- MCP/A2A deferred with security caveat — documented in `AGENT_STACK_EVALUATION.md`.

No security blockers.

---

## Reliability and ops

- `/healthz` returns 200 (smoke).
- Structured logging in API startup (`main.py`).
- RAG health exposes configuration + tier metadata for operator visibility.
- Explicit fallback policy documented and implemented in RAG service.

**Nit:** API must be manually restarted before demo; documented in HANDOFF/DEMO_CHECKLIST.

---

## Performance

Not materially changed in this pass. Synthetic corpus (~28 docs) suitable for demo. No N+1 or hot-path concerns identified in review scope.

---

## Tests and verification

| Check | Result |
|-------|--------|
| `uv run pytest -q` | 33 passed |
| `pnpm run build` | OK |
| API smoke matrix | 10/10 HTTP 200 |
| RAG tier assertions | Present in `test_rag.py`; live `/api/rag/health` matches |

**Missing (acceptable for doc pass):** No tests for buyer-agent (not implemented). No E2E browser test for UI — manual walkthrough documented.

Definition of Done: docs + CHANGELOG updated; health endpoint present; pytest green — **met for current scope**.

---

## Docs and DX

- Authoritative agent + local AI docs exist and cross-link from README, AGENTS, HANDOFF.
- Fixed drift: `REPRODUCTION_GUIDE` version, `VALIDATION_REPORT`, `DEMO_CHECKLIST`, API version 0.5.4.
- `FINAL_STATUS` and HANDOFF verification log updated in this pass.

---

## Findings

| ID | Severity | Location | Recommendation |
|----|----------|----------|----------------|
| F1 | should-fix | (fixed) `config.py`, `.env.example` | Was `0.5.0` vs docs `0.5.4` — bumped to 0.5.4 in this pass |
| F2 | should-fix | (fixed) `REPRODUCTION_GUIDE.md` | Was `0.5.2` header — updated |
| F3 | nit | MVP vs roadmap | Buyer agent chat not in UI — do not claim live in pitch; use runbook talking points |
| F4 | nit | `GUIDED_SIMULATION_DESIGN.md` | Linear sim remains; LangGraph target documented — OK for demo |
| F5 | nit | Deploy | Production API + scanovich.ai still ops next step per HANDOFF |

No open **blocker** findings after F1/F2 fixes.

---

## Verdict

**Ready for hackathon demo** — deterministic settlement flow, six scenarios, developer hub mismatch story, and documentation stack (local AI + agent architecture) are consistent and verified.

**Recommended next build:** Scaffold `apps/buyer-agent/` per `BUYER_CONSULTATION_AGENT.md` and `REPRODUCTION_GUIDE.md` Phase J.

---

## Related

- [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) — smoke results
- [`HANDOFF.md`](HANDOFF.md) — verification log
- [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md) — presenter order
