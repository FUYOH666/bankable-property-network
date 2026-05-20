# Handoff — Bankable Property Network

Living document for session continuity and new-chat onboarding. **Version: 0.5.5**

## New chat starter (copy-paste)

```text
Project: Bankable Property Network (hackathon MVP).
Read AGENTS.md and docs/HANDOFF.md first.
Stack: apps/api (FastAPI, uv), apps/web (Next.js, pnpm), data/synthetic/.
Current version: 0.5.5. Do not edit .cursor/plans/.
Continue from "Next Work" section in HANDOFF.
```

## Product snapshot

| Concept | Description |
|---------|-------------|
| Primary customer | Banking anchor / regulated money-serving structures |
| Social bonus | Buyer deposit protection when infrastructure works |
| Anchor case | 12M THB condo, payee mismatch (`SRL Holding 2026` vs `Siam Riverside Living Co., Ltd.`) |
| Web3 use | Metadata-only evidence attestation — not property tokenization |

## Implemented modules (0.5.x)

- Verified Developer Knowledge Layer — feed + hub API/UI
- Settlement Flow panel — single fetch from `/api/demo/closing-passport`
- Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport
- Post-Closing Yield Plan (vision stub)
- Guided Deal Simulation + Evidence Pack JSON export
- Scenario Simulator — 8 scenarios with RAG trace
- Supplier Contrast Demo — off-platform vs tier-1 developer supply panel
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

Architecture diagram: [`ARCHITECTURE.md`](ARCHITECTURE.md)

Developer Knowledge Layer: [`DEVELOPER_KNOWLEDGE_LAYER.md`](DEVELOPER_KNOWLEDGE_LAYER.md)

## Verification log

**Last verified:** 2026-05-20 (full cycle + staff review)

```text
pytest:  37 passed (apps/api)
build:   pnpm run build OK (apps/web)
api_version: 0.5.5 (config.py + .env.example)

Smoke (localhost:8080) — 12/12 HTTP 200:
  healthz, closing-passport, developer-knowledge-hub, supplier-contrast,
  guided-simulation, evidence-pack, post-closing-yield-plan,
  scenarios (count=8), prelaunch-off-platform-route/run,
  tier-one-landmark-route/run,
  usdt-mixed-route/rag-run?mode=fallback,
  rag/health (tier metadata OK)

Staff review: docs/STAFF_REVIEW_0.5.4.md — verdict: ready for hackathon demo
Known gap: buyer-agent chat not live (roadmap)
```

### Restart commands

```bash
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
cd apps/api && uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080

cd apps/web && pnpm dev
```

## Recent architectural decisions

- **Bank-first narrative** — not a buyer-education app
- **Developer Knowledge upstream** — SSOT before Property Shield
- **Routing invariant** — `bankable_escrow` always recommended; `pick_recommended_route()` prevents StopIteration
- **UI single source** — Settlement Flow panel replaces static capital/route cards
- **Out of scope for hackathon** — live WhatsApp/Telegram/TTS, multi-tenant ingestion port
- **Agent architecture (doc 0.5.4)** — LangGraph.js primary; Buyer Consultation Agent + Settlement Branch Explorer documented; not implemented in code yet

## Next work (priority)

1. **Buyer Consultation Agent scaffold** — `apps/buyer-agent/` LangGraph.js + LM Studio local contour — [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md)
2. **Deploy API** — follow [`DEPLOY.md`](DEPLOY.md), set `BANKABLE_CORS_ORIGINS` for scanovich.ai
3. **Website publish** — [`PUBLISH_SEABLOCKCHAINWEEK.md`](PUBLISH_SEABLOCKCHAINWEEK.md), `NEXT_PUBLIC_SEABW_API_URL` at build time
4. **PDF Closing Passport** — downloadable bank-ready artifact (optional)
5. **2-Week Pilot** — developer feed ingestion, role-based views — see [`ROADMAP.md`](ROADMAP.md)

## Doc index (start here)

| Doc | Use |
|-----|-----|
| [`../AGENTS.md`](../AGENTS.md) | Agent entry point |
| [`REPRODUCTION_GUIDE.md`](REPRODUCTION_GUIDE.md) | Rebuild from zero + expansion matrix |
| [`FINAL_STATUS_AND_NEXT_ACTIONS.md`](FINAL_STATUS_AND_NEXT_ACTIONS.md) | Human status |
| [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md) | Presenter flow |
| [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md) | 3-minute script |
| [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) | Local AI stack startup (Qdrant, BGE, LM Studio) |
| [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md) | Demo vs enterprise AI tier matrix |
| [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) | Settlement Branch Explorer / bank graph |
| [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) | Nonlinear buyer consultation layer |
| [`AGENT_STACK_EVALUATION.md`](AGENT_STACK_EVALUATION.md) | LangGraph.js primary; framework filter |
| [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md) | Developer supply contrast pitch (Shadow Bay vs tier-1) |
| [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md) | AI/hackathon auditor entry — live vs roadmap, invariants |
| [`PROJECT_DESCRIPTION.md`](PROJECT_DESCRIPTION.md) | Hackathon registration copy (EN) |
| [`STAFF_REVIEW_0.5.4.md`](STAFF_REVIEW_0.5.4.md) | Latest verification + staff review |
| [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) | Smoke matrix + demo gaps |
| [`PITCH_SCRIPT.md`](PITCH_SCRIPT.md) | Pitch lines |
| [`DEPLOY.md`](DEPLOY.md) | Docker / Render |

## Environment variables

See [`.env.example`](../.env.example). Key vars:

- `BANKABLE_CORS_ORIGINS` — production CORS
- `NEXT_PUBLIC_SEABW_API_URL` / `NEXT_PUBLIC_BANKABLE_API_URL` — web → API
- `BANKABLE_LOG_LEVEL`, `BANKABLE_API_VERSION` — API config
- `QDRANT_URL`, `LOCAL_AI_*` — optional live RAG (demo tier: BGE + LM Studio; production: vLLM + Qwen-class — see `AI_SERVICE_TIERS.md`)
- `BANKABLE_AI_TIER` — health metadata (`demo_local` default)
