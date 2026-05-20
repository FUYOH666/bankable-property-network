# Changelog

## v1.0.0-pivot.w0.sim — 2026-05-20 (branch `v1/attestation-layer`)

**Full local simulation unlocks autonomous Week 1.** No faucet, no manual
schema registration needed. Everything runs on an Anvil fork of Base
Sepolia that inherits real EAS protocol bytecode at canonical addresses.

### What changed

- Installed Foundry 1.7.1 (forge / cast / anvil / chisel).
- Authored `scripts/dev-chain.sh` (idempotent) — spins up Anvil fork of
  Base Sepolia on port 8545, verifies EAS contract, registers the
  `SettlementApproval` schema via SchemaRegistry, writes `.dev-chain.state`.
- Authored `scripts/stop-dev-chain.sh` — clean shutdown by pid file or
  port lookup.
- Documented full simulation in `docs/v1/DEV_SIMULATION.md` (Anvil default
  account map, architecture diagram, smoke test, switch to real testnet
  in Week 3).
- Verified end-to-end: stop → start cycle = ~19 s, schema verified via
  `getSchema(uid)` readback, deterministic UID
  `0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96`.
- Updated `.env.example` with dev + production mode blocks. Dev attester
  key explicitly marked as the public Anvil test key (never use on
  mainnet).
- Updated `.gitignore` for `.dev-chain.state`, `.env.dev`, Foundry build
  artefacts, and Anvil logs.
- Marked the previous "manual blocker" in `WEEK0_BOOTSTRAP.md` as no
  longer blocking. The faucet step survives only as an optional Week 3
  task for public-testnet visibility (or skipped entirely with a recorded
  demo).
- Filled live registration data in `docs/v1/ATTESTATION_SCHEMA.md` §3a
  (dev fork) and §3b placeholder (real Base Sepolia Week 3).

### Why fork-not-mock

A pure Anvil node would have required us to deploy mock EAS / SchemaRegistry
contracts ourselves. Forking Base Sepolia gives us the real protocol bytecode
at the canonical addresses (`0x4200…0021`, `0x4200…0020`), so all behaviour —
event topics, gas, revert messages, ABI — is identical to production. The
escrow contract we build in Week 2 will not need any code path changes when
we switch from local fork to real testnet in Week 3.

## v1.0.0-pivot.w0 — 2026-05-20 (branch `v1/attestation-layer`)

**GODMODE pivot — Week 0 bootstrap.** This is the start of a radical
repositioning from "Bankable Property Network" (B2B bank settlement
infrastructure for Thailand property) to **AttestRWA** (Settlement
Attestation Layer for RWA) — a web3-native on-chain compliance bridge for
stablecoin real-world-asset settlements, targeting SEA Blockchain Week
2026.

Full plan: `.cursor/plans/godmode-pivot-attestation-layer_*.plan.md`.

### What changed

- Branched `v1/attestation-layer` from `main@7148ac5` (v0.5.13). `main`
  stays as safety until `v1.0.0` is ready to merge.
- Created `archive/v0.5/` scaffold; legacy modules will be moved here in
  Week 1 via `git mv` (commit history preserved).
- Created `contracts/` Foundry workspace skeleton (Week 2 fills in
  `SettlementEscrow.sol` + `MockUSDC.sol` + fuzz tests).
- Drafted new root README in `docs/v1/README_DRAFT.md` with the AttestRWA
  hook, pivot story, on-chain artefact table, and Week 0–3 roadmap.
- Defined EAS Schema `SettlementApproval` in
  `docs/v1/ATTESTATION_SCHEMA.md` — schema string, field semantics,
  threat model stub, registration instructions, escrow integration sketch.
- Documented Week 0 bootstrap state and the single manual step
  (generate attester EOA, fund on Base Sepolia, register schema) in
  `docs/v1/WEEK0_BOOTSTRAP.md`.

### Decisions locked (Week 0)

| Slot | Value |
|------|-------|
| Brand | AttestRWA |
| Network | Base Sepolia (chainId 84532) |
| Stablecoin | Mock USDC ERC-20 (own deployment) |
| Contracts | Foundry (fuzz + invariants + slither) |
| Wallet stack | wagmi + viem + RainbowKit |
| Buyer consult fate | Archive to `archive/v0.5/` |
| Timeline | 1–3 weeks "divine" mode |
| Demo | Live testnet + 3 pre-funded deals + 60s backup video |

### Next (blocking Week 1)

User must complete manual steps in `docs/v1/WEEK0_BOOTSTRAP.md` §A–D:

1. Generate attester EOA (`cast wallet new`).
2. Fund on Base Sepolia (Alchemy / QuickNode faucet).
3. Register `SettlementApproval` schema on Base Sepolia EAS.
4. Report Schema UID + attester address back.

After that: Week 1 surgery (archive legacy, rebrand, slim docs, extend
synthetic data) starts.

## 0.5.13 - 2026-05-20

- Full project audit: [`docs/PROJECT_AUDIT_REPORT.md`](docs/PROJECT_AUDIT_REPORT.md) — system map, LIVE vs ROADMAP, effectiveness re-score, P0/P1/P2 backlog.
- Tier A doc sync to 0.5.13: AI_AUDIT_INDEX, VALIDATION_REPORT, FINAL_STATUS, PROJECT_DESCRIPTION, DOCS_AUDIT, runbooks, scorecard, NEXT_BUILD_PRIORITY; REPRODUCTION_GUIDE version section.
- `developer_knowledge` channel_roadmap: WhatsApp and web → `live`.
- Scenario/dialogue report scripts stamp API v0.5.13.

## 0.5.12 - 2026-05-20

- Fix SYSTEM_PROMPT leak in WhatsApp consult: rewritten prompt, `_is_prompt_leak` sanitizer, deterministic `_purchase_pitch_reply` for USDT/cash/mixed capital questions.
- Synthetic RAG: `capital_routes_buyer_pitch.md`, `thailand_property_reference_links.md`; extended `Buyer_Settlement_Bridge.md` with Landmark → bank rails pitch.
- Dialogue matrix +3 scripts (`usdt_buyer_ru`, `cash_buyer_ru`, `mixed_capital_en`); pytest for prompt-leak and purchase pitch fallback.
- `WHATSAPP_CONSULT_DEMO.md` 4-turn jury arc including USDT product pitch turn.

## 0.5.11 - 2026-05-20

- Consult KB pivot: removed legacy Karon/TEST DEVELOPER 1 corpus; replaced with slim **Landmark Sukhumvit Tower** KB (Bangkok Landmark Group, 18.5–24.8M THB).
- Aligned WhatsApp demo narrative with settlement/supplier contrast (Bangkok tier-1, not Phuket).
- Updated `buyer_consultation.py` anchors, greetings, villa handler, scenario strip regex; dialogue matrix 14/14 (offline uses keyword mode for CI determinism).
- Docs: `WHATSAPP_CONSULT_DEMO.md` 3-turn distribution script; `CONSULT_KNOWLEDGE_DEMO.md` without RealEstate-AI import.

## 0.5.10 - 2026-05-20

- Documentation sync: Tier A docs aligned to v0.5.10 (58+ pytest, 14/14 dialogue matrix, consult live LLM).
- Multi-channel narrative: `docs/DISTRIBUTION_CHANNELS.md` — one `POST /api/consult/message`, WhatsApp live; Telegram, Line, email, voice roadmap.
- Consult KB bridge: `Buyer_Settlement_Bridge.md`, `FAQ_TH.md`; policy `consult_channel_policy.md`; extended dialogue matrix (`mixed_project_settlement`, `follow_up_context`).
- Intent fix: strip `TEST DEVELOPER` before scenario keyword detection; FET template snippet for Russian/English FAQ turns.
- Cross-links: PITCH, RUNBOOK, ARCHITECTURE, BUYER_CONSULTATION_AGENT, DEMO_CHECKLIST, SYNTHETIC_CORPUS.

## 0.5.9 - 2026-05-20

- Consult dialogue simulation: `scripts/run_consult_dialogue_matrix.py` + `data/consult_dialogues/dialogue_matrix.yaml` (offline + live API modes).
- Agent tuning: expanded project intent (villa/buy/where), consult_kb-only RAG filter, session-aware retrieval, structured LLM context, WhatsApp reply sanitization.
- Qwen 3.6 in LM Studio: `LOCAL_AI_LLM_ENABLE_THINKING=false` (default) + `chat_template_kwargs` for direct `content` replies.
- Demo anchor: TEST DEVELOPER 1 / Karon Phuket enforced in prompts; villa requests get honest condo inventory answer.
- Report: `docs/CONSULT_DIALOGUE_SIMULATION_REPORT.md`; tests in `test_consult_dialogue_matrix.py`.

## 0.5.8 - 2026-05-20

- Full local AI contour for buyer consult: Qdrant + BGE embed/rerank + LM Studio wired in Docker via `host.docker.internal`.
- RAG ingest includes `data/consult_knowledge/realestate-demo/` alongside synthetic corpus; `consult_retrieval.py` with `CONSULT_RETRIEVAL_MODE` (`auto` | `keyword` | `rag`).
- Buyer consultation uses RAG pipeline with explicit keyword fallback; citations include `retrieval_mode` and `rerank_score`.
- API: `GET /api/consult/contour/healthz`; `scripts/start-full-ai-contour.sh`; docker-smoke checks contour + LLM configured.
- Docs: updated `LOCAL_AI_CONTOUR.md`, `CONSULT_KNOWLEDGE_DEMO.md`, `HACKATHON_RUNBOOK.md`, `AI_AUDIT_INDEX.md`, `DOCKER_QUICKSTART.md`.

## 0.5.7 - 2026-05-20

- WhatsApp bridge: message ID dedup (fixes duplicate replies); `/pair` auto-refresh QR page.
- Consult knowledge: import RealEstate-AI `knowledge_base` → `data/consult_knowledge/realestate-demo/`; `consult_knowledge.py` keyword chunk search (no Qdrant).
- Buyer consultation: intent routing (greeting / project_faq / settlement / mixed), multilingual greetings, conditional bank tools.
- API: `GET /api/consult/knowledge/healthz`; consult response includes `intent`.
- Docs: `docs/CONSULT_KNOWLEDGE_DEMO.md`; ASR voice roadmap; `scripts/import_realestate_knowledge.sh`.

## 0.5.6 - 2026-05-20

- Added batch scenario simulation: `scripts/run_scenario_matrix.py` → `docs/SCENARIO_SIMULATION_REPORT.md` (all 8 scenarios, judge-ready grouping).
- Buyer Consultation API: `POST /api/consult/message`, `GET /api/consult/healthz`; `buyer_consultation.py` with internal tools, LM Studio instruct path, explicit template fallback.
- WhatsApp bridge MVP: `services/whatsapp-bridge/` (Go + whatsmeow), QR pairing on `:8020`, wired to consult API; `infra/docker-compose.yml` services `bankable-api` + `whatsapp-bridge`.
- UI: `buyer-consultation-panel.tsx` web fallback chat.
- Docs: `docs/WHATSAPP_CONSULT_DEMO.md`; runbook/checklist WhatsApp steps; `AI_AUDIT_INDEX` buyer consult partial live.

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
- Hackathon demo vitrine: https://scanovich.ai/seablockchainweek/ (static showcase; removable post-event).

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
