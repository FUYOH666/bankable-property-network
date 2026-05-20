# Buyer Consultation Agent

## Role

The **Buyer Consultation Agent** helps a purchaser explore a property, understand capital options, and navigate toward a bankable settlement path.

It **does not** approve payments, release escrow, or override deterministic bank rules.

## Why Nonlinear

Real buyers exhibit non-linear behavior:

- Start with property details, jump to agent trust, return to deposit urgency
- Ask about USDT before understanding FET requirements
- Switch language, topic, and urgency mid-conversation
- Abandon a branch and re-enter later

A linear chatbot fails here. A **LangGraph.js state graph** supports conditional routing, suspend/resume, and re-entry without losing context.

## Architecture Position

```mermaid
flowchart TB
  buyer[Buyer]
  agent[BuyerConsultationAgent]
  lmStudio[LMStudio_local]
  tools[PolicyControlledTools]
  api[BankableAPI_8080]
  graph[SettlementDecisionGraph]

  buyer --> agent
  agent -.-> lmStudio
  agent --> tools
  tools --> api
  api --> graph
```

| Component | Location | Purpose |
|-----------|----------|---------|
| Consultation graph | Future `apps/buyer-agent/` | LangGraph.js orchestration |
| LLM | LM Studio `:1234/v1` (demo) | Natural language, schema-bound replies |
| Evidence tools | BGE + Qdrant via API | Policy/developer corpus retrieval |
| Bank tools | FastAPI `:8080` | Property Shield, scenarios, developer hub |
| Decision graph | Bankable Property OS | Authoritative settlement (see [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md)) |

## Constructor Pattern

Graph-as-code — not a no-code toy:

- **Nodes** — intake, property Q&A, capital Q&A, route exploration, handoff
- **Edges** — conditional on state (e.g. `capital_status`, `payee_aligned`, `user_intent`)
- **State schema** — Zod-validated shared state across turns
- **Debug** — LangGraph Studio / step trace for audit and demo rehearsal

Example state slice (documentation only):

```typescript
{
  session_id: string;
  property_id?: string;
  capital_sources: string[];
  payee_question_raised: boolean;
  last_node: string;
  citations: Array<{ document_id: string; excerpt: string }>;
  handoff_requested: boolean;
}
```

## Local Contour Integration

All agent inference runs in the **local demo contour**. See [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md).

| Service | Port | Agent usage |
|---------|------|-------------|
| LM Studio | `:1234/v1` | Consultation LLM (primary consumer in demo) |
| BGE embedding | `:9001` | RAG tool backend via API |
| Qdrant | `:6333` | Vector retrieval |
| Bankable API | `:8080` | Policy-controlled tools only |

Production tier: LM Studio → **vLLM gateway**; see [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

**Security principle:** tools are **API endpoints**, not shell, browser, or filesystem access. No «agent does things on machine».

## Tool Surface

Documented contract for future implementation (not live in hackathon MVP):

```text
get_developer_knowledge_hub()
  → GET /api/demo/developer-knowledge-hub

retrieve_policy_evidence(query)
  → RAG retrieve over synthetic corpus (via API wrapper)

run_scenario_preview(scenario_id)
  → GET /api/scenarios/{id}/run or rag-run

get_property_shield_summary()
  → Derived from closing-passport / settlement flow payload

request_human_handoff(reason)
  → Suspend graph; log reason; surface compliance contact
```

Each tool returns structured JSON validated against Zod schemas before the LLM synthesizes a buyer-facing reply.

## Guardrails

| Rule | Enforcement |
|------|-------------|
| No hallucinated payees | Citations required from developer hub or RAG |
| No payment instructions on RED | Block template responses; escalate |
| Schema-bound outputs | Pydantic/Zod for structured fields |
| Explicit unknown | Prefer «evidence not found» over invention |
| No KYC collection | Agent does not store passport/PII in graph state |

## UI Pattern (AG-UI Inspired)

Without adopting the full AG-UI protocol, the web layer can stream **node status events**:

```text
Checking developer entity...
Verifying payment instruction...
Classifying capital source...
Comparing settlement routes...
Generating escrow conditions preview...
```

Future panel: `apps/web/src/agent/` or embedded chat beside Settlement Flow.

## Boundaries

The Buyer Consultation Agent is **not**:

- KYC/KYB verification
- Legal or tax advice
- Autonomous escrow or payment execution
- A replacement for verified agency channels (see [`DEVELOPER_KNOWLEDGE_LAYER.md`](DEVELOPER_KNOWLEDGE_LAYER.md))

It **is** a guided, evidence-backed exploration layer that hands off to bank-grade settlement when the buyer is ready.

## Recommended Code Location

| Phase | Path |
|-------|------|
| Scaffold | `apps/buyer-agent/` — standalone LangGraph.js service |
| Embedded UI | `apps/web/src/agent/` — Next.js chat panel calling buyer-agent |

Reproduction steps: [`REPRODUCTION_GUIDE.md`](REPRODUCTION_GUIDE.md) Phase J.

## Related

- [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) — bank settlement graph
- [`AGENT_STACK_EVALUATION.md`](AGENT_STACK_EVALUATION.md) — LangGraph.js primary rationale
- [`JOURNEY_BUYER.md`](JOURNEY_BUYER.md) — buyer journey with consultation step
