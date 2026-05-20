# Changelog

## 0.5.5 - 2026-05-20

- Added Developer Supply Demo: Shadow Bay prelaunch (off-platform) vs Bangkok Landmark Group (fictional tier-1 on-network).
- Synthetic feeds, policies, RAG docs, and `project-landmark-tower`; enriched `project-shadow-red`.
- New scenarios: `prelaunch-off-platform-route`, `tier-one-landmark-route`; `supply_risk_signals` on scenario runs.
- New API: `GET /api/demo/supplier-contrast`; refactored `developer_knowledge.py` for parameterized feed paths.
- UI: Supplier Contrast panel (`supplier-contrast-demo.tsx`), pitch card «Why Developers Join», scenario simulator labels.
- Docs: `docs/DEVELOPER_SUPPLY_DEMO.md`; cross-links in PITCH_SCRIPT, DEMO_CHECKLIST, HACKATHON_RUNBOOK, SCENARIO_MATRIX, SYNTHETIC_CORPUS, README, HANDOFF.
- Added `docs/PROJECT_DESCRIPTION.md` for hackathon registration; synced doc drift (8 scenarios, v0.5.5) across AGENTS, FINAL_STATUS, REPRODUCTION_GUIDE, VALIDATION_REPORT, DOCS_AUDIT, PUBLISH.
- Added `docs/AI_AUDIT_INDEX.md` for automated/hackathon project review; aligned DEMO_SCRIPT, DEMO_REHEARSAL_REPORT, SYNTHETIC_DATA_GUIDE, JOURNEY_DEVELOPER_AGENT, ARCHITECTURE.
- Published public repository: https://github.com/FUYOH666/bankable-property-network (Apache-2.0).

## 0.5.4 - 2026-05-20

- Added agent architecture documentation: `docs/NONLINEAR_DECISION_GRAPH.md` (Settlement Branch Explorer), `docs/BUYER_CONSULTATION_AGENT.md` (LangGraph.js buyer layer), `docs/AGENT_STACK_EVALUATION.md` (framework filter).
- Cross-linked README, AGENTS.md, ARCHITECTURE, LOCAL_AI_CONTOUR, AI_SERVICE_TIERS, THESIS, journeys, ROADMAP, REPRODUCTION_GUIDE (Phase J buyer agent), HANDOFF, HACKATHON_RUNBOOK, PITCH_SCRIPT, DOCS_AUDIT, FINAL_STATUS.
- Documented LangGraph.js as primary orchestration; buyer agent and settlement graph as roadmap (doc-first, no code scaffold yet).
- **Verification pass:** 33 pytest, frontend build, 10/10 API smoke; `docs/STAFF_REVIEW_0.5.4.md`; aligned API version to 0.5.4 in `config.py` and `.env.example`; updated VALIDATION_REPORT, DEMO_CHECKLIST, REPRODUCTION_GUIDE.

## 0.5.3 - 2026-05-20

- Added local AI contour documentation: `docs/LOCAL_AI_CONTOUR.md` (Qdrant + BGE + LM Studio runbook) and `docs/AI_SERVICE_TIERS.md` (demo vs enterprise matrix: vLLM, Qwen-class embeddings).
- Extended `GET /api/rag/health` with tier metadata (`deployment_tier`, `embedding_tier`, `llm_tier`, `production_note`).
- Updated `.env.example`, `config/default.yaml`, Developer Knowledge Hub `ai_stack`, and cross-links across README, ARCHITECTURE, REAL_RAG_DEMO, THESIS, REPRODUCTION, HANDOFF, DEPLOY, HACKATHON_RUNBOOK.

## 0.5.2 - 2026-05-20

- Verified stack end-to-end: 33 pytest, frontend build, all demo endpoints smoke OK.
- Added agent handoff package: `AGENTS.md`, `docs/HANDOFF.md`, `.cursor/rules/bankable-project.mdc`.
- Added `docs/REPRODUCTION_GUIDE.md` — single-file rebuild playbook with phase order and per-module expansion matrix.
- Updated VALIDATION_REPORT, PUBLISH_SEABLOCKCHAINWEEK, DOCS_AUDIT, JOURNEY_BUYER, JOURNEY_DEVELOPER_AGENT, `.env.example`.

## 0.5.1 - 2026-05-20

- Staff review polish: shared `paths.py` + `data_loader`, routing invariant fix, structured logging, Pydantic settings/schemas, API version 0.5.0.
- Settlement Flow panel replaces static capital/route/passport cards; `useDemoFetch` hook; demo flow aligned across README, runbooks, and UI.
- Added tests for routing edge cases, paths, data loader, scenario 404s, developer hub aligned payee (33 tests total).

## 0.5.0 - 2026-05-20

- Added Verified Developer Knowledge Layer: synthetic developer feed, policy doc, `GET /api/demo/developer-knowledge-hub`, Developer Knowledge Hub vision screen.
- Documented upstream SSOT model in `docs/DEVELOPER_KNOWLEDGE_LAYER.md`; updated thesis, README network layers, ROADMAP, and PITCH_SCRIPT.
- Pitch screen card for Developer Knowledge Hub; payee mismatch vs anchor case in demo.

## 0.4.0 - 2026-05-20

- Added commission model synthetic policy doc for RAG corpus.
- Added API `infrastructure_context` on demo endpoints; production CORS for scanovich.ai via `BANKABLE_CORS_ORIGINS`.
- Reframed `page.tsx` hero and anchor case under money infrastructure thesis.
- Aligned DEMO_SCRIPT, JOURNEY_BUYER, DEMO_CHECKLIST, FINAL_STATUS, VALIDATION_REPORT, ROADMAP.
- Added DEPLOY.md, PUBLISH_SEABLOCKCHAINWEEK.md, Dockerfile, render.yaml; `NEXT_PUBLIC_SEABW_API_URL` env alias.

## 0.3.0 - 2026-05-20

- Reframed project narrative around money infrastructure thesis: banks and regulated structures as primary customers, buyer protection as social bonus.
- Added `docs/MONEY_INFRASTRUCTURE_THESIS.md` with commission-model root problem, brand gap, and AI operational layer.
- Updated NETWORK_POSITIONING, PITCH_SCRIPT, STAKEHOLDER_PERSPECTIVES, ARCHITECTURE, README, HACKATHON_RUNBOOK, and Pitch Screen UI.

## 0.2.0 - 2026-05-20

- Added Post-Closing Yield Plan strategic extension: `GET /api/demo/post-closing-yield-plan`, web vision screen, synthetic rental managers and building restrictions.
- Documented Bankable Property & Yield OS in README and pitch script.

## 0.1.0 - 2026-05-19

- Created Bankable Property OS hackathon MVP scaffold.
- Added Closing Passport backend demo endpoint.
- Added Property Shield, Capital Bankability Map, route comparison, and evidence pack hashing.
- Added synthetic anchor case for risky property deposit with legal entity mismatch.
- Added demo UI, documentation pack, Qdrant compose file, and environment template.
- Reframed the project as Bankable Property Network with Bankable Property OS as the operating layer and Closing Passport as the first module.
- Added production roadmap, scenario matrix, role journeys, and synthetic corpus for SWIFT, USDT, cash/P2P, mixed capital, developer risk, and agent risk scenarios.
- Added Scenario API, deterministic RAG trace stub, frontend scenario simulator, pitch docs, synthetic evidence documents, rehearsal report, and hackathon runbook.
- Added real RAG integration with Qdrant REST, local embedding/reranker services, retrieved evidence UI, explicit fallback mode, and live RAG run report.
- Added polished web pitch screen and updated demo runbook/checklist/status documentation for final judging flow.
