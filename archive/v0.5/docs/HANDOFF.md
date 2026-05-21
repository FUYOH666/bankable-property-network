# Handoff — Bankable Property Network

Living document for session continuity and new-chat onboarding. **Version: 0.5.13**

## New chat starter (copy-paste)

```text
Project: Bankable Property Network (hackathon MVP).
Read AGENTS.md and docs/HANDOFF.md first.
Stack: apps/api (FastAPI, uv), apps/web (Next.js, pnpm), data/synthetic/.
Current version: 0.5.13. Do not edit .cursor/plans/.
Consult inventory: Landmark Sukhumvit Tower (Bangkok), not Karon/Phuket legacy.
Continue from "Next Work" section in HANDOFF.
```

## Context budget (read order when tokens are tight)

| Tier | Read | Why |
|------|------|-----|
| 0 | This file + [`AGENTS.md`](../AGENTS.md) + [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) | Version, audit, verification, backlog |
| 1 | [`CHANGELOG.md`](../CHANGELOG.md) (top 3 entries) | What changed recently |
| 2 | [`buyer_consultation.py`](../apps/api/src/app/services/buyer_consultation.py) | Live consult brain (intent, pitch, leak guard) |
| 3 | [`dialogue_matrix.yaml`](../data/consult_dialogues/dialogue_matrix.yaml) | 17-turn regression contract |
| 4 | [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md) | Booth 4-turn jury arc |

Skip unless task-specific: full `REPRODUCTION_GUIDE.md`, old Karon corpus, `.cursor/plans/`.

## Product snapshot

| Concept | Description |
|---------|-------------|
| Primary customer | Banking anchor / regulated money-serving structures |
| Social bonus | Buyer deposit protection when infrastructure works |
| Consult layer | Distribution channel — same API on WhatsApp, web, curl; Telegram/Line/email/voice roadmap |
| Consult inventory | **Landmark Sukhumvit Tower** (Bangkok Landmark Group, 18.5–24.8M THB) — `data/consult_knowledge/realestate-demo/` |
| Settlement anchor | 12M THB condo, payee mismatch (`SRL Holding 2026` vs `Siam Riverside Living Co., Ltd.`) — bank demo, separate from consult KB |
| Web3 use | Metadata-only evidence attestation — not property tokenization |

## Implemented modules (0.5.x)

- Verified Developer Knowledge Layer — feed + hub API/UI
- Settlement Flow panel — single fetch from `/api/demo/closing-passport`
- Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport
- Post-Closing Yield Plan (vision stub)
- Guided Deal Simulation + Evidence Pack JSON export
- Scenario Simulator — 8 scenarios with RAG trace
- Supplier Contrast Demo — off-platform vs tier-1 developer supply panel
- **Buyer Consultation (live)** — `buyer_consultation.py`, WhatsApp bridge, web panel; Qdrant + BGE + LM Studio
  - Intent: greeting / project_faq / settlement / mixed
  - **USDT/cash/mixed pitch** — `_purchase_pitch_reply` + `_is_prompt_leak` (0.5.12)
  - RAG: 46 docs (39 synthetic + 7 consult_kb); policies incl. `capital_routes_buyer_pitch.md`
  - Dialogue matrix **17/17** (9 scripts, offline keyword mode for CI)
- Shared infra: `paths.py`, `data_loader.py`, Pydantic demo schemas, structured logging

## API contract

| Method | Path | Response highlights |
|--------|------|---------------------|
| GET | `/healthz` | `{ status: "ok" }` |
| GET | `/api/demo/closing-passport` | `property_shield`, `capital_bankability_map`, `routes`, `closing_passport` |
| GET | `/api/demo/developer-knowledge-hub` | `knowledge_vs_agent_gap.status` → `mismatch_detected` on anchor |
| GET | `/api/demo/supplier-contrast` | Side-by-side Shadow Bay vs Bangkok Landmark tracks |
| GET | `/api/demo/guided-simulation` | `steps[]`, `closing_passport` |
| GET | `/api/demo/evidence-pack` | Privacy-safe JSON export |
| GET | `/api/demo/post-closing-yield-plan` | Yield OS vision |
| GET | `/api/scenarios` | 8 scenario ids |
| GET | `/api/scenarios/{id}/rag-run` | Scenario run + RAG trace |
| POST | `/api/rag/ingest` | Re-index synthetic + consult_kb → Qdrant |
| POST | `/api/consult/message` | `{ session_id, channel, message }` → intent, reply, retrieval_mode, tools_used, citations |
| GET | `/api/consult/healthz` | Consult stack status |
| GET | `/api/consult/contour/healthz` | Qdrant + BGE + LM Studio readiness |

Architecture diagram: [`ARCHITECTURE.md`](ARCHITECTURE.md) · Channels: [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md)

## Verification log

**Last verified:** 2026-05-20 (v0.5.13 audit)

```text
pytest:  64 passed (apps/api)
dialogue_matrix: 17/17 offline (9 scripts; CONSULT_RETRIEVAL_MODE=keyword)
rag_ingest: 46 documents (39 synthetic + 7 consult_kb)
build:   pnpm run build OK (apps/web)
api_version: 0.5.13 (config.py + .env.example)

Consult: live FastAPI + WhatsApp + web; LM Studio when LOCAL_AI_LLM_INSTRUCT_BASE_URL set
Fallback: purchase_pitch_template for USDT/cash/mixed when LLM leaks or unavailable
Contour: GET /api/consult/contour/healthz → all_ready before booth
LangGraph buyer-agent: roadmap (docs only)
```

### Quick regression

```bash
cd apps/api && uv run pytest -q
cd apps/api && CONSULT_RETRIEVAL_MODE=keyword uv run python ../../scripts/run_consult_dialogue_matrix.py --offline
curl -X POST http://localhost:8080/api/rag/ingest   # after KB/policy changes
```

### Restart commands

```bash
# Full Docker stack (API + WhatsApp + Qdrant)
./scripts/docker-up.sh

# Local AI contour on host (BGE + LM Studio) + Docker API
./scripts/start-full-ai-contour.sh

lsof -ti:8080 | xargs kill -9 2>/dev/null || true
cd apps/api && uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080

cd apps/web && pnpm dev
```

## Recent architectural decisions

- **Bank-first narrative** — consult is distribution, not payment authority
- **One consult brain** — `POST /api/consult/message` + channel adapters ([`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md))
- **Landmark consult KB** (0.5.11) — slim Bangkok corpus; removed Karon/TEST DEVELOPER 1
- **USDT purchase pitch** (0.5.12) — deterministic pitch + prompt-leak sanitizer
- **developer_knowledge channels** (0.5.13) — WhatsApp/web marked live in API payload
- **consult_kb RAG filter** — project FAQ uses `data/consult_knowledge/realestate-demo/` only
- **Explicit fallback** — keyword/template/purchase_pitch when BGE/Qdrant/LM unavailable; logged `retrieval_mode`
- **LangGraph.js** — documented target; FastAPI consult is live MVP

## Next work (priority)

See [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) §11 and [`NEXT_BUILD_PRIORITY.md`](NEXT_BUILD_PRIORITY.md).

1. **Booth readiness** — docker-smoke, contour all_ready, 60s backup recording, scanovich deploy
2. **P1 polish** — consult judge mode (retrieval_mode + citations), PitchScreen API outcomes
3. **LangGraph scaffold** — `apps/buyer-agent/` — [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md)
4. **Channel adapters** — Telegram / Line thin wrappers
5. **Production WhatsApp** — Meta Business API
6. **Settlement Branch Explorer UI** — [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md)
7. **Doc drift CI** — `scripts/audit-docs.sh` (optional)

## Doc index (start here)

| Doc | Use |
|-----|-----|
| [`../AGENTS.md`](../AGENTS.md) | Agent entry point |
| [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md) | Multi-channel consult |
| [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md) | Dialogue regression (17/17) |
| [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md) | Booth 4-turn arc incl. USDT pitch |
| [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md) | AI/hackathon auditor entry |
| [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) | Qdrant + BGE + LM Studio |
| [`CONSULT_KNOWLEDGE_DEMO.md`](CONSULT_KNOWLEDGE_DEMO.md) | Consult KB + intent routing |
| [`SYNTHETIC_CORPUS.md`](SYNTHETIC_CORPUS.md) | Corpus layout + ingest counts |
| [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) | Full audit — LIVE vs ROADMAP, backlog |
| [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md) | 3-minute script + demo arc |

## Environment variables

See [`.env.example`](../.env.example). Key vars:

- `LOCAL_AI_LLM_INSTRUCT_BASE_URL` — LM Studio (Qwen 3.6; set `LOCAL_AI_LLM_ENABLE_THINKING=false`)
- `LOCAL_AI_EMBEDDING_BASE_URL`, `LOCAL_AI_RERANKER_BASE_URL` — BGE services
- `QDRANT_URL` — vector store for RAG + consult
- `CONSULT_RETRIEVAL_MODE` — `auto` | `keyword` | `rag`
