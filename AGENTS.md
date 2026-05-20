# AGENTS.md — Bankable Property Network

Bank-grade money infrastructure for Thailand property. **Primary customer:** banking anchor and regulated structures. Buyer protection is a social bonus.

- **Network:** Bankable Property Network
- **OS:** Bankable Property OS (FastAPI + Next.js demo)
- **First module:** Closing Passport (evidence before funds move)
- **Upstream layer:** Verified Developer Knowledge Layer (developer ERP feed as SSOT)
- **Agent layers (roadmap):** Buyer Consultation Agent + Settlement Branch Explorer — LangGraph.js
- **Thesis:** [`docs/MONEY_INFRASTRUCTURE_THESIS.md`](docs/MONEY_INFRASTRUCTURE_THESIS.md)
- **AI / hackathon audit:** [`docs/AI_AUDIT_INDEX.md`](docs/AI_AUDIT_INDEX.md) — start here for automated project review
- **Registration:** [`docs/PROJECT_DESCRIPTION.md`](docs/PROJECT_DESCRIPTION.md)

## Stack

| Layer | Path | Tooling |
|-------|------|---------|
| API | `apps/api` | Python 3.12+, **uv**, FastAPI |
| Web | `apps/web` | **pnpm**, Next.js 16 |
| Buyer agent (roadmap) | `apps/buyer-agent` | **pnpm**, LangGraph.js, Zod, LM Studio |
| Data | `data/synthetic/` | JSON + markdown corpus for demo/RAG |
| Vector DB | `infra/docker-compose.yml` | Qdrant (optional for live RAG) |

Local AI contour for agent LLM + RAG: [`docs/LOCAL_AI_CONTOUR.md`](docs/LOCAL_AI_CONTOUR.md). Agent architecture: [`docs/NONLINEAR_DECISION_GRAPH.md`](docs/NONLINEAR_DECISION_GRAPH.md), [`docs/BUYER_CONSULTATION_AGENT.md`](docs/BUYER_CONSULTATION_AGENT.md).

## Commands

```bash
# API
cd apps/api && uv sync && uv run pytest -q
cd apps/api && uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080

# Web
cd apps/web && pnpm install && pnpm dev
cd apps/web && pnpm run build

# Health
curl http://localhost:8080/healthz
```

## Demo flow (UI order)

1. Pitch Screen
2. Supplier Contrast (off-platform prelaunch vs tier-1 on-network)
3. Developer Knowledge Hub (upstream SSOT vs agent payee)
4. Anchor case cards
5. Settlement Flow panel — Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport
6. Post-Closing Yield Plan
7. Guided Deal Simulation
8. Scenario Simulator (8 scenarios incl. developer supply paths)
9. Footer demo steps recap

Presenter checklist: [`docs/DEMO_CHECKLIST.md`](docs/DEMO_CHECKLIST.md)

## Key API endpoints

| Path | Purpose |
|------|---------|
| `GET /healthz` | Liveness |
| `GET /api/demo/closing-passport` | Full settlement flow payload |
| `GET /api/demo/developer-knowledge-hub` | Developer feed vs agent gap |
| `GET /api/demo/supplier-contrast` | Off-platform vs tier-1 developer supply contrast |
| `GET /api/demo/guided-simulation` | Step-by-step workflow |
| `GET /api/demo/evidence-pack` | Exportable JSON evidence |
| `GET /api/demo/post-closing-yield-plan` | Yield OS vision |
| `GET /api/scenarios` | Eight synthetic scenarios |
| `GET /api/scenarios/{id}/rag-run` | Scenario + RAG trace |

## Key code paths

- API entry: `apps/api/src/app/main.py`
- Paths/data: `apps/api/src/app/paths.py`, `services/data_loader.py`
- Closing demo builder: `services/closing_passport_demo.py`
- Web fetch hook: `apps/web/src/lib/use-demo-fetch.ts`
- Settlement UI: `apps/web/src/app/closing-passport-panel.tsx`

## Conventions

- Python: **uv only** (no pip), `logging` not `print`, `/healthz` required
- Data loading: `load_json()` from `data_loader` — do not duplicate `Path(__file__).parents[N]`
- Web: `useDemoFetch()` + `getApiBaseUrl()` for all demo API calls
- User-facing changes: update `CHANGELOG.md` and relevant docs

## Do not

- Commit secrets, `.env`, or TailScale/internal IPs
- Edit files under `.cursor/plans/`
- Use `pip install` without uv
- Claim live WhatsApp/TTS channels (roadmap only)

## Continue development

Read **[`docs/HANDOFF.md`](docs/HANDOFF.md)** for version, verification log, API contract, and next work.

Rebuild from zero or onboard parallel team: **[`docs/REPRODUCTION_GUIDE.md`](docs/REPRODUCTION_GUIDE.md)**.

Status summary: [`docs/FINAL_STATUS_AND_NEXT_ACTIONS.md`](docs/FINAL_STATUS_AND_NEXT_ACTIONS.md)

## New chat starter

```text
Project: Bankable Property Network (hackathon MVP).
Read AGENTS.md and docs/HANDOFF.md first.
Stack: apps/api (FastAPI, uv), apps/web (Next.js, pnpm), data/synthetic/.
Current version: 0.5.5. Do not edit .cursor/plans/.
Continue from "Next Work" section in HANDOFF.
```
