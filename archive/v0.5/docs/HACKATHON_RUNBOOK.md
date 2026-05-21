# Hackathon Runbook

## Start API

```bash
cd apps/api
uv sync
uv run uvicorn app.main:app --app-dir src --host 0.0.0.0 --port 8080
```

## Start Web

```bash
cd apps/web
pnpm install
pnpm dev
```

Open the web app at the URL printed by Next.js.

## Smoke Endpoints

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
curl -X POST http://localhost:8080/api/consult/message -H 'Content-Type: application/json' -d '{"session_id":"smoke","message":"payee mismatch","channel":"web"}'
curl http://localhost:8080/api/scenarios/swift-clean-route/run
curl http://localhost:8080/api/scenarios/usdt-mixed-route/run
curl http://localhost:8080/api/scenarios/cash-red-route/run
curl http://localhost:8080/api/scenarios/mixed-capital-route/run
curl http://localhost:8080/api/scenarios/developer-suspicious-route/run
curl http://localhost:8080/api/scenarios/agent-risk-route/run
curl http://localhost:8080/api/scenarios/prelaunch-off-platform-route/run
curl http://localhost:8080/api/scenarios/tier-one-landmark-route/run
```

## Real RAG Demo

**Local AI contour (2 min for judges):** Start full stack with `./scripts/start-full-ai-contour.sh` — Docker Qdrant, BGE embedding/reranker on MacBook, LM Studio for buyer consult. WhatsApp → consult agent: project FAQ via Qdrant + BGE + reranker; money questions via bank API + policy RAG. LM Studio explains in buyer language — never approves deposits. Explicit fallback when any service is down. Verify: `curl http://localhost:8080/api/consult/contour/healthz`. Full runbook: [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) · consult KB: [`CONSULT_KNOWLEDGE_DEMO.md`](CONSULT_KNOWLEDGE_DEMO.md) · tiers: [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

Start Qdrant:

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
```

Index synthetic evidence:

```bash
curl -X POST http://localhost:8080/api/rag/ingest
```

Run scenario with retrieval:

```bash
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run"
```

If services are unavailable, run explicit fallback:

```bash
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run?mode=fallback"
```

## Demo Order — 3-Minute Script

### 0:00–0:40 — Brand And Structural Gap

Open with the thesis:

> Thailand's property market runs on developer-paid commissions with no professional entry barrier. Bankable Property Network introduces the verification and settlement infrastructure the Kingdom's brand promise requires.

Explain:

- Kingdom brand = institutional-grade; market reality = unverified intermediaries, money off bankable rails.
- Primary customer = banking anchor / money-serving structures. Buyer story = demo illustration.

### 0:40–1:20 — Money OS And AI Layer

**Nonlinear decision graph (30 sec):** This is not a chatbot — it is a settlement decision graph. Settlement Branch Explorer runs parallel capital routes, scores cost/FET/compliance/buyer protection, and converges on bankable escrow with Closing Passport. Buyer Consultation Agent (LangGraph.js, local contour) handles non-linear buyer dialogue without settlement authority. Docs: [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md), [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).

Explain the naming:

- Bankable Property Network: full platform vision.
- Bankable Property OS: operating layer for money in property.
- Closing Passport: first module — evidence before funds move.

AI line:

> AI does not decide whether money moves. AI helps regulated structures review evidence faster, at scale, with traceability.

### 1:20–2:20 — Live Demo

Show Pitch Screen (structural problem, money OS, **Why Developers Join**, brand alignment, social bonus).

**Supplier contrast (45 sec):** Off-platform prelaunch hides permit and payee gaps — Shadow Bay sells before permits, no Closing Passport. On-network tier-1 (Bangkok Landmark Group, fictional) publishes ERP feed; bank sees green path. Full script: [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md).

Show **Supplier Contrast** panel — Shadow Bay vs Bangkok Landmark side-by-side.

Show **Developer Knowledge Hub** — agent payee vs developer ERP feed (`mismatch_detected` on anchor case).

Show anchor case as **infrastructure failure** — not naive buyer story:

- 12M THB Bangkok condo;
- Dubai bank funds + USDT;
- unverified settlement path;
- payee legal entity differs from expected developer.

Show **Settlement Flow** panel (Property Shield, Capital Map, Route Comparison, Bank Counter-Offer, Closing Passport — live API).

Show Post-Closing Yield Plan vision screen.

Show Guided Deal Simulation and Scenario Simulator (eight scenarios):

- SWIFT clean: green, approve, Closing Passport generated.
- USDT mixed: amber, conditional approval.
- Mixed capital: mixed status, conditional approval.
- Cash/P2P red: reject, no normal Closing Passport.
- Suspicious developer: green capital but property risk escalates.
- Agent risk: agent risk escalates route.
- Prelaunch off-platform: prelaunch without permit, no Closing Passport.
- Tier-1 Landmark: verified feed, approve, Closing Passport generated.

Show RAG Trace and Retrieved Evidence when available.

### 2:20–2:50 — Multi-Stakeholder Value

- Bank: capture flow, escrow/compliance, long-term relationship.
- Compliance: structured gate, audit trail.
- State/brand: traceable inflows, market quality alignment.
- Verified participants: differentiation from commission-only intermediaries.
- Buyer: social bonus — deposit protection on bankable rails.

### 2:50–3:00 — Close

> Everyone is building faster ways to move money. We are building the layer that decides whether money should move, through which route, and under what verified conditions.

> Most platforms stop when the property is sold. Banks should not.

> Settlement OS without truth upstream is incomplete. Developer SSOT → verified agents → bank rails → Closing Passport → Yield OS.

## Legacy Demo Order (Reference)

1. Open with the thesis (see 3-minute script above).

2. Explain the naming:

   - Bankable Property Network: full platform.
   - Bankable Property OS: operating layer.
   - Closing Passport: first module.

3. Show the anchor case:

   - foreign buyer;
   - 12M THB Bangkok condo;
   - Dubai bank funds + USDT;
   - urgent deposit pressure;
   - mismatched payee legal entity.

4. Show Pitch Screen:

   - problem;
   - solution;
   - four scenario outcomes;
   - retrieved evidence;
   - bank/public value;
   - roadmap.

5. Show Guided Deal Simulation.

6. Show Scenario Simulator:

   - SWIFT clean: green, approve, Closing Passport generated.
   - USDT mixed: amber, conditional approval.
   - Cash/P2P red: reject, no normal Closing Passport.
   - Suspicious developer: green capital but property risk escalates.

7. Show RAG Trace:

   - policy document;
   - developer profile;
   - agent profile;
   - payment instruction;
   - route rule;
   - compliance memo.
   - retrieved evidence and reranker scores when live RAG is available.

8. Show Evidence Pack JSON.

9. Close with:

   > Everyone is building faster ways to move money. We are building the layer that decides whether money should move, through which route, and under what verified conditions.

## If API Is Down

Use static docs:

- `docs/PITCH_SCRIPT.md`;
- `docs/SCENARIO_MATRIX.md`;
- `docs/DEMO_REHEARSAL_REPORT.md`;
- `docs/PRODUCTION_ROADMAP.md`;
- `docs/SYNTHETIC_CORPUS.md`.

Tell the story as a controlled simulation and show the synthetic corpus.

## If Asked About AI/RAG

Answer:

> AI does not decide whether money moves. The demo uses deterministic rules plus a controlled RAG pipeline — Qdrant, embeddings, reranking, schema-validated LLM explainability — so regulated structures can review evidence faster at scale. When services are unavailable, explicit fallback mode applies. Decisions remain evidence-backed, traceable, and human-in-loop. The product direction is a **nonlinear decision graph** (Settlement Branch Explorer) plus a separate **Buyer Consultation Agent** — not a linear property chatbot.

Optional future demo: live buyer-agent chat against LM Studio in local contour (not required for hackathon MVP).

**Full AI contour (live now):** `./scripts/start-full-ai-contour.sh` — consult calls LM Studio + RAG when services are up; check `retrieval_mode: llm_instruct` or `rag_llm` in `/api/consult/message` response.

## Demo Story Arc (3 min + WhatsApp)

| Step | UI / channel | API / action | Judge line |
|------|--------------|--------------|------------|
| 1 | Pitch Screen | — | Commission market has no verification layer |
| 2 | Supplier Contrast | `GET /api/demo/supplier-contrast` | Off-platform prelaunch vs tier-1 feed |
| 3 | Developer Knowledge Hub | `GET /api/demo/developer-knowledge-hub` | Payee mismatch — upstream SSOT |
| 4 | Settlement Flow | `GET /api/demo/closing-passport` | Bank decides route before funds move |
| 5 | Scenario Simulator | `GET /api/scenarios/{id}/rag-run` | Eight capital paths, explicit RAG/fallback |
| 6 | WhatsApp (optional) | consult bridge → `POST /api/consult/message` | **4-turn arc:** greeting → price/villa → **USDT «как покупать?»** → payee guardrail |
| 7 | Close | — | WhatsApp today; Line/TG/email/voice tomorrow — one API |

Channels: [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md) · dialogue evidence: [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md).

## WhatsApp Consultation (60 sec)

**4-turn jury arc** — full script: [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md).

| Turn | Message | Pitch |
|------|---------|-------|
| 1 | «привет» | Distribution — channel, not payment authority |
| 2 | price / villa | Landmark Bangkok condos |
| 3 | **«а как покупать? у меня usdt»** | Amber capital → bank rails, not agent wallet |
| 4 | wire to agent? | Payee guardrail — do not deposit |

30-second line: USDT is not a shortcut around the bank — it is amber capital needing conversion evidence, verified payee, FET, and Land Department registration on bankable rails.

Message the consultant on WhatsApp — same synthetic API as the web fallback panel:

```bash
docker compose -f infra/docker-compose.yml up -d bankable-api whatsapp-bridge
open http://localhost:8020/qr   # scan once before booth
curl http://localhost:8020/status
```

Script line:

> The buyer layer cites developer feeds and scenario facts from our API. It never approves a deposit — banks stay on bankable rails. If WhatsApp is flaky, use the web consultation panel.

Full setup: [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md) · scenario batch report: [`SCENARIO_SIMULATION_REPORT.md`](SCENARIO_SIMULATION_REPORT.md).

## If Asked About Legal/KYC

Answer:

> We do not replace lawyers, KYC providers, regulators, land offices, or banks. We provide settlement readiness, risk evidence, escrow conditions, and auditability. Final regulated decisions remain human-in-the-loop.

## Final Checks Before Presenting

```bash
cd apps/api && uv run pytest
cd apps/web && pnpm typecheck && pnpm build
```

Expected:

- backend tests pass;
- frontend typecheck/build pass;
- at least 4 scenario outcomes are explainable in 30 seconds each.
