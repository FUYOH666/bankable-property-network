# Next Implementation Sprints

## Sprint 1: Documentation And Synthetic Universe

Status: completed in documentation form.

Deliverables:

- production roadmap;
- scenario matrix;
- synthetic projects, agents, buyers, banks, documents, and scenarios;
- role-based journey docs;
- README links.

## Sprint 2: Scenario API

Goal:

Expose the synthetic corpus through deterministic API endpoints.

Deliverables:

- `GET /api/scenarios`;
- `GET /api/scenarios/{scenario_id}`;
- deterministic route decision for SWIFT, USDT, cash/P2P, and mixed capital;
- RAG trace stub per scenario;
- evidence pack export per scenario.

Verification:

- tests for clean SWIFT route;
- tests for amber USDT route;
- tests for red cash/P2P route;
- tests that sensitive fields are absent.

## Sprint 3: UI Scenario Simulator

Goal:

Let judges or bank stakeholders choose scenarios and see different outcomes.

Deliverables:

- scenario picker;
- buyer view;
- bank officer view;
- compliance view;
- route decision;
- evidence pack export;
- RAG trace panel.

Verification:

- frontend typecheck and build;
- at least 3 scenarios visible in UI;
- each scenario displays a different capital status and route decision.

## Sprint 4: Production Narrative

Goal:

Show that the product can scale beyond a demo.

Deliverables:

- pitch screen;
- bank benefit view;
- government/public value view;
- business model view;
- pilot metrics dashboard mock.

Verification:

- 3-minute pitch script updated;
- stakeholder objections documented;
- no legal/title/KYC overclaim.

## Sprint 5: Controlled AI/RAG Pilot

Goal:

Connect the scenario simulator to local or controlled AI/RAG services.

Deliverables:

- Qdrant ingest script for synthetic corpus;
- embedding and reranker clients;
- retrieval trace;
- LLM explanation with structured schema;
- deterministic fallback if services are unavailable.

Verification:

- health checks for API and service dependencies;
- retrieval trace contains document IDs;
- LLM output validates against schema;
- fallback is explicit and logged.

## Sprint 6: Buyer Consultation Agent Graph

Goal:

Scaffold nonlinear buyer consultation layer with LangGraph.js in local contour.

Deliverables:

- `apps/buyer-agent/` — LangGraph.js service with Zod state schema;
- tools wrapping FastAPI demo endpoints (developer hub, scenario preview, RAG evidence);
- LM Studio via OpenAI-compatible client;
- `/healthz` on buyer-agent service;
- AG-UI-inspired status streaming stub in web (optional).

Verification:

- graph handles branch jumps (property → capital → back to property);
- no payment instruction on RED aggregate;
- citations required for payee claims;
- handoff node logs reason.

See [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md), [`AGENT_STACK_EVALUATION.md`](AGENT_STACK_EVALUATION.md).

## Sprint 7: Settlement Branch Explorer UI

Goal:

Visualize parallel settlement branches and aggregator scores in demo UI.

Deliverables:

- branch comparison panel fed by scenario matrix + route engine;
- score dimensions: cost, FET, AML, buyer protection, bank revenue;
- link to Closing Passport on selected branch.

Verification:

- eight scenarios map to visible branch inputs (incl. developer supply paths);
- selected branch matches deterministic API outcome.

See [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md), [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md).
