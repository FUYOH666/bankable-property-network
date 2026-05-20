# Demo Checklist

## Start Services

API:

```bash
cd apps/api
uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080
```

Web:

```bash
cd apps/web
pnpm dev
```

Production API CORS (when deploying):

```bash
BANKABLE_CORS_ORIGINS=https://scanovich.ai,http://localhost:3000
```

## Smoke Checks

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/api/demo/closing-passport
curl http://localhost:8080/api/demo/developer-knowledge-hub
curl http://localhost:8080/api/demo/supplier-contrast
curl http://localhost:8080/api/demo/guided-simulation
curl http://localhost:8080/api/demo/evidence-pack
curl http://localhost:8080/api/demo/post-closing-yield-plan
curl http://localhost:8080/api/scenarios
curl http://localhost:8080/api/rag/health
curl http://localhost:8080/api/consult/healthz
curl http://localhost:8080/api/consult/contour/healthz
curl -X POST http://localhost:8080/api/consult/message -H 'Content-Type: application/json' -d '{"session_id":"smoke","message":"payee mismatch","channel":"web"}'
curl http://localhost:8080/api/scenarios/swift-clean-route/run
curl http://localhost:8080/api/scenarios/cash-red-route/run
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run?mode=fallback"
```

Optional live RAG (local contour — see [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md)):

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
# Start BGE embedding :9001 and reranker :9002
curl -X POST http://localhost:8080/api/rag/ingest
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run"
```

RAG health should expose tier metadata (`deployment_tier`, `embedding_tier`, `llm_tier`). Enterprise tiers: [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

## WhatsApp Consultation (optional booth)

Before the booth opens:

```bash
docker compose -f infra/docker-compose.yml up -d bankable-api whatsapp-bridge
open http://localhost:8020/qr
```

Scan QR once with WhatsApp → Linked devices. Full runbook: [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md).

## Presenter Talking Points (optional)

- **Registration copy:** [`PROJECT_DESCRIPTION.md`](PROJECT_DESCRIPTION.md) — problem, solution, value, copy-paste blocks for platform forms.
- **AI audit entry:** [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md) — live vs roadmap, invariants, doc tiers for automated reviewers.
- **Local AI contour (30 sec):** [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) · [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md)
- **Nonlinear decision graph (30 sec):** [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) · [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md)

Note: Buyer Consultation is **live** via API, web panel, and WhatsApp bridge — see [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md), [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md). LangGraph.js orchestration remains roadmap.

## Show In Demo (Money Infrastructure Order)

1. Open with structural gap thesis (`docs/MONEY_INFRASTRUCTURE_THESIS.md` one-liner).
2. Show Pitch Screen: Structural Problem, Money OS, Developer Knowledge Hub card, **Why Developers Join**, Brand Alignment, Social Bonus.
3. Show **Supplier Contrast** — Shadow Bay prelaunch vs Bangkok Landmark tier-1 (`docs/DEVELOPER_SUPPLY_DEMO.md`).
4. Show Developer Knowledge Hub — payee mismatch vs developer feed.
5. Show anchor case as infrastructure failure illustration.
6. Show Settlement Flow panel (Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport).
7. Show Post-Closing Yield Plan.
8. Show Guided Deal Simulation.
9. Show Scenario Simulator — eight scenarios with RAG trace when available (includes `prelaunch-off-platform-route`, `tier-one-landmark-route`).
10. Open Evidence Pack JSON from Guided Simulation.
11. Close with multi-stakeholder value and production roadmap.

## Production Publish

See `docs/PUBLISH_SEABLOCKCHAINWEEK.md` for scanovich.ai `/seablockchainweek/` handoff.

## Fallback Story

If live API is unavailable:

- `docs/PITCH_SCRIPT.md`
- `docs/SCENARIO_MATRIX.md`
- `docs/SYNTHETIC_CORPUS.md`
- `docs/PRODUCTION_ROADMAP.md`

## Do Not Claim

- Legal title guarantee.
- Replacement of KYC/KYB providers.
- Regulator approval.
- Agent licensing.
- Full production compliance.
- Property NFT ownership.
- Live buyer consultation agent or LangGraph chat (documented roadmap only).
