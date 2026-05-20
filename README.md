# Bankable Property Network

[![Version](https://img.shields.io/badge/version-0.5.13-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Stack](https://img.shields.io/badge/stack-FastAPI%20%2B%20Next.js-000)](apps/api)

Bank-grade money infrastructure for Thailand property.

**Author:** [Aleksandr Mordvinov](https://github.com/FUYOH666) · **Repository:** [github.com/FUYOH666/bankable-property-network](https://github.com/FUYOH666/bankable-property-network) · **Demo:** [scanovich.ai/seablockchainweek](https://scanovich.ai/seablockchainweek/) _(hackathon vitrine)_

## Pitch

Thailand's property market runs on developer-paid commissions with no professional entry barrier. Intermediaries are not verified for skills, local law, FET requirements, or payee authority. Money often moves off bankable rails while the Kingdom brand promise expects institutional-grade settlement.

Bankable Property Network is the infrastructure layer that closes that gap — **for banks and regulated structures first**, for national market quality second. Buyer protection is a social bonus, not the product mission.

`Bankable Property OS` is the operating layer. `Closing Passport` is the first MVP module: it verifies a property purchase context before money moves, including property and developer risk, payment instructions, buyer capital bankability, settlement route, compliance approval, and metadata-only evidence attestation.

The strategic extension is **Bankable Property & Yield OS**: after closing, verified rental operations, legal rental mode guidance, and bank rental income accounts turn a one-time purchase into a long-term asset relationship.

SCB can be the first banking anchor in the pitch, but the network can expand to Bangkok Bank, Kasikorn, Krungsri, UOB, HSBC, Dubai banks, Singapore banks, and other settlement participants.

See `docs/MONEY_INFRASTRUCTURE_THESIS.md` for the full money infrastructure thesis.

**Agent / new chat:** read [`AGENTS.md`](AGENTS.md), [`docs/HANDOFF.md`](docs/HANDOFF.md), and [`docs/PROJECT_AUDIT_REPORT.md`](docs/PROJECT_AUDIT_REPORT.md) for full project state.

**Hackathon registration:** copy-paste from [`docs/PROJECT_DESCRIPTION.md`](docs/PROJECT_DESCRIPTION.md).

**AI / automated project audit:** start with [`docs/AI_AUDIT_INDEX.md`](docs/AI_AUDIT_INDEX.md).

## Hackathon Demo

Anchor case **illustrates infrastructure failure** when money is about to move through an unverified path: a 12M THB Bangkok condo, Dubai bank funds and USDT, deposit pressure, payment instructions pointing to a legal entity that differs from the expected developer.

The demo shows:

1. Pitch Screen explains the problem, solution, scenario outcomes, evidence layer, bank value, and roadmap.
2. **Supplier Contrast** — off-platform prelaunch (Shadow Bay) vs tier-1 on-network (Bangkok Landmark Group).
3. Developer Knowledge Hub compares agent payee instruction against developer ERP feed (upstream SSOT).
4. Settlement Flow panel: Property Shield, Capital Bankability Map, Route Comparison, Bank Counter-Offer, Closing Passport (live API).
5. Post-Closing Yield Plan shows Bankable Property & Yield OS vision.
6. Guided Deal Simulation walks buyer → bank → compliance → passport.
7. Scenario Simulator runs eight synthetic capital/property/agent/supply scenarios with RAG trace.
8. **Buyer Consultation** — multi-channel API (`channel` param), WhatsApp live, web panel; Landmark Sukhumvit consult KB; USDT/cash purchase pitch with prompt-leak guard; Qdrant + BGE + LM Studio contour. See [`docs/DISTRIBUTION_CHANNELS.md`](docs/DISTRIBUTION_CHANNELS.md), [`docs/WHATSAPP_CONSULT_DEMO.md`](docs/WHATSAPP_CONSULT_DEMO.md), [`docs/CONSULT_DIALOGUE_SIMULATION_REPORT.md`](docs/CONSULT_DIALOGUE_SIMULATION_REPORT.md).

Guided Simulation and Scenario Simulator extend the anchor case; steps 2–4 are the core money-infrastructure path.

## Docker (API + WhatsApp — start here for booth)

```bash
chmod +x scripts/docker-up.sh scripts/docker-smoke.sh
./scripts/docker-up.sh
open http://localhost:8020/qr    # scan with WhatsApp → Linked devices
./scripts/docker-smoke.sh        # API + consult + scenario smoke
```

Full guide: [`docs/DOCKER_QUICKSTART.md`](docs/DOCKER_QUICKSTART.md) · WhatsApp booth: [`docs/WHATSAPP_CONSULT_DEMO.md`](docs/WHATSAPP_CONSULT_DEMO.md).

Full local AI contour: [`scripts/start-full-ai-contour.sh`](scripts/start-full-ai-contour.sh) · [`docs/LOCAL_AI_CONTOUR.md`](docs/LOCAL_AI_CONTOUR.md).

Consult dialogue regression (17/17 offline, 9 scripts):

```bash
cd apps/api && CONSULT_RETRIEVAL_MODE=keyword uv run python ../../scripts/run_consult_dialogue_matrix.py --offline
```

```bash
uv run python scripts/run_scenario_matrix.py --api-url http://localhost:8080
```

## Network Layers

- Verified Developer Knowledge Layer (upstream SSOT — inventory, payee, installments from developer ERP feed).
- Verified Property Layer.
- Verified Developer Layer (settlement identity and payee authority on rails).
- Verified Agent Layer.
- Buyer Capital Layer.
- Settlement Routing Layer.
- Escrow and Conditional Release.
- Closing Passport.
- Post-Purchase Financial Layer (Yield OS vision screen).

## Marketplace Positioning

Bankable Property Network is not another listing marketplace. Listing platforms help buyers discover property. Bankable Property Network gives **structures that serve money** the operating layer to verify whether funds should move, through which route, and under what evidence-backed settlement conditions.

## Agent Architecture

Nonlinear orchestration for bank settlement and buyer consultation — **LangGraph.js primary**. See [`docs/NONLINEAR_DECISION_GRAPH.md`](docs/NONLINEAR_DECISION_GRAPH.md), [`docs/BUYER_CONSULTATION_AGENT.md`](docs/BUYER_CONSULTATION_AGENT.md), [`docs/AGENT_STACK_EVALUATION.md`](docs/AGENT_STACK_EVALUATION.md).

## Production Planning

- `docs/MONEY_INFRASTRUCTURE_THESIS.md`: money OS thesis, brand gap, commission model, AI layer.
- `docs/HANDOFF.md`: agent session continuity, verification log, next work.
- `docs/REPRODUCTION_GUIDE.md`: rebuild from zero, phase order, expansion matrix per module.
- `docs/DEVELOPER_KNOWLEDGE_LAYER.md`: verified developer feed as upstream SSOT, channel roadmap, Property Shield linkage.
- `docs/AI_AUDIT_INDEX.md`: entry point for AI/hackathon project auditors (live vs roadmap, invariants).
- `docs/PROJECT_DESCRIPTION.md`: hackathon registration copy (problem, solution, value, copy-paste blocks).
- `docs/DEVELOPER_SUPPLY_DEMO.md`: off-platform prelaunch vs tier-1 on-network supplier contrast pitch.
- `docs/PUBLISH_SEABLOCKCHAINWEEK.md`: handoff for scanovich.ai/seablockchainweek/ demo publish.
- `docs/DEPLOY.md`: FastAPI Docker and Render deploy guide.
- `docs/PRODUCTION_ROADMAP.md`: production-grade rollout from hackathon demo to 12-month platform.
- `docs/SCENARIO_MATRIX.md`: SWIFT, USDT, cash/P2P, mixed capital, developer risk, agent risk, and supply demo scenarios.
- `docs/SYNTHETIC_CORPUS.md`: synthetic projects, buyers, agents, banks, documents, and scenarios.
- `docs/NEXT_IMPLEMENTATION_SPRINTS.md`: build sequence for scenario API, UI simulator, production narrative, and controlled AI/RAG pilot.
- `docs/PITCH_SCRIPT.md`: 60-second and 3-minute pitch.
- `docs/OBJECTION_HANDLING.md`: bank, government, legal, KYC, blockchain, marketplace objections.
- `docs/DEMO_CHECKLIST.md`: startup commands and demo flow.
- `docs/HACKATHON_RUNBOOK.md`: final runbook for launching and presenting the demo.
- `docs/DEMO_REHEARSAL_REPORT.md`: automated checks and four scenario rehearsal outcomes.
- `docs/REAL_RAG_DEMO.md`: Qdrant + local embedding/reranker demo flow.
- `docs/LOCAL_AI_CONTOUR.md`: local demo stack runbook (Qdrant, BGE, LM Studio).
- `docs/AI_SERVICE_TIERS.md`: demo vs enterprise AI tier matrix (vLLM, Qwen-class embeddings).
- `docs/REAL_RAG_RUN_REPORT.md`: latest live RAG ingestion and scenario run evidence.
- `docs/NONLINEAR_DECISION_GRAPH.md`: Settlement Branch Explorer / bank decision graph.
- `docs/BUYER_CONSULTATION_AGENT.md`: nonlinear buyer consultation agent (LangGraph.js roadmap).
- `docs/AGENT_STACK_EVALUATION.md`: agent framework filter; LangGraph.js primary.
- `docs/DOCKER_QUICKSTART.md`: one-command Docker stack (API + WhatsApp + scenario smoke).
- `docs/CONSULT_KNOWLEDGE_DEMO.md`: two-layer consult KB (project + bank), intent routing, ASR roadmap.
- `docs/DISTRIBUTION_CHANNELS.md`: one consult brain, many channel adapters (WhatsApp live; Telegram, Line, email, voice roadmap).

## Project Layout

```text
apps/api        FastAPI backend for rules, evidence, and demo endpoint
apps/web        Next.js demo UI
data/synthetic  Synthetic property, developer, policy, and settlement docs
data/consult_knowledge/realestate-demo/  Landmark Sukhumvit consult KB (RAG filter: consult_kb)
docs            Demo script, architecture, roadmap, value model; HANDOFF.md for session continuity
infra           Docker Compose (API, WhatsApp bridge, Qdrant)
config          Source-controlled non-secret config
```

## Run The API

```bash
cd apps/api
uv sync
uv run pytest
uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080
```

Health check:

```bash
curl http://localhost:8080/healthz
```

Demo endpoint:

```bash
curl http://localhost:8080/api/demo/closing-passport
curl http://localhost:8080/api/demo/developer-knowledge-hub
curl http://localhost:8080/api/demo/supplier-contrast
curl http://localhost:8080/api/demo/guided-simulation
curl http://localhost:8080/api/demo/evidence-pack
curl http://localhost:8080/api/demo/post-closing-yield-plan
```

Scenario and RAG endpoints:

```bash
curl http://localhost:8080/api/scenarios
curl http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run
curl -X POST "http://localhost:8080/api/rag/ingest?dry_run=true"
curl -X POST http://localhost:8080/api/consult/message \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"demo","message":"а как покупать? у меня usdt","channel":"whatsapp"}'
```

## Run The Web Demo

```bash
cd apps/web
pnpm install
pnpm dev
```

The web demo reads live Closing Passport data from `NEXT_PUBLIC_BANKABLE_API_URL`, defaulting to `http://localhost:8080`. Start the API first to show the real generated evidence hash in the UI.

## Run Qdrant

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
```

## Environment

Copy `.env.example` to `.env` and replace placeholder service URLs with your local or controlled-environment endpoints. Do not commit `.env`.

## Privacy And Web3 Position

We do not tokenize the property. We tokenize the evidence of a verified settlement process.

The Closing Passport stores status metadata and an evidence pack hash. It must not store passports, contracts, bank statements, private wallet ownership data, or personal data on-chain.
