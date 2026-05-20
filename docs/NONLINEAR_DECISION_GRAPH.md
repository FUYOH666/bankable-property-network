# Nonlinear Decision Graph

## Thesis

> This is not a chatbot.
> It is a **nonlinear decision graph** for bankable property settlement.

Bankable Property OS models settlement as a **state graph** with conditional routing, parallel branch exploration, human gates, and auditable artifacts — not a linear Q&A flow.

## Settlement Branch Explorer

**Product name:** Settlement Branch Explorer  
**Internal engine:** Nonlinear Capital Routing Engine

The system explores multiple settlement realities in parallel, scores each branch, and converges on a bankable route with escrow conditions and Closing Passport evidence.

```text
Buyer Intent
  ├─ Property Risk Shield
  ├─ Capital Bankability Map
  ├─ Agent / Developer Verification
  └─ Settlement Route Auction
        ↓
Risk Aggregator
  ├─ RED → Reject / Escalate
  ├─ AMBER → Human Review / Missing Docs
  └─ GREEN → Bank Counter-Offer
        ↓
Escrow Conditions
        ↓
Closing Passport
        ↓
Audit / Attestation
        ↓
Post-Closing Yield Plan
```

## Graph Nodes

Each node maps to existing MVP modules or API endpoints today.

| Node | Maps to today | Role |
|------|---------------|------|
| Intake | Guided simulation step 1 | Collect buyer, property, and capital intent |
| Property Shield Agent | `closing_passport_demo` / Property Shield | Developer, seller, agent, payment instruction, deposit terms |
| Capital Bankability Agent | Capital Bankability Map | Classify sources green / amber / red |
| Settlement Route Agent | Route comparison + 8 scenarios | Build parallel settlement branches |
| FlowCapture Agent | Counter-offer narrative | Show where bank loses flow if buyer uses P2P |
| Counter-Offer Agent | Bank counter-offer payload | FET-ready proposal, corrected payee |
| Escrow Agent | Escrow conditions | Conditional release rules |
| Closing Passport Agent | `GET /api/demo/closing-passport` | Evidence pack hash and metadata |
| Yield Agent | `GET /api/demo/post-closing-yield-plan` | Post-closing rental / yield vision |

## Branch-and-Merge Pattern

Settlement Route Agent spawns parallel branches:

```text
Route A: Dubai Bank → Thai Bank → FET-ready settlement
Route B: USDT liquidation → foreign currency remittance → Thai Bank
Route C: P2P THB route
Route D: Hybrid route (mixed capital)
Route E: Reject / legal review route
```

Each branch receives scores across dimensions:

| Dimension | Question |
|-----------|----------|
| cost | Total fees and spread |
| speed | Time to closing |
| FET readiness | Foreign exchange transaction compliance |
| AML risk | Source-of-funds traceability |
| buyer protection | Payee authority, escrow, dispute path |
| bank revenue | Captured settlement flow vs P2P leak |
| closing certainty | Probability of successful close |
| developer confidence | Alignment with developer authorized feed |

**Risk Aggregator** compares branches and selects or recommends a bankable path. Human compliance gates apply before release.

## Nonlinear Transitions

| Condition | Transition |
|-----------|------------|
| Property risk = RED | Block payment; escalate to legal / compliance |
| Capital = AMBER | Request additional documents; suspend graph |
| Payee mismatch detected | Block release; surface Developer Knowledge Hub delta |
| P2P cheaper but FET weak | Show P2P Risk Mirror (FlowCapture) |
| Bank route too expensive | Generate counter-offer node |
| Buyer is investor | Add Yield Agent module |
| Developer verified in feed | Allow escrow route candidate |
| Payment account mismatch | Hard block on fund release |

Users and buyers do not follow linear scripts. The graph supports **re-entry**: jump from capital questions back to property verification, then forward to route comparison.

## Human Gates

Money never releases autonomously from an LLM node.

| Gate | Trigger |
|------|---------|
| Compliance approval | AMBER capital or elevated property flags |
| Missing documents | Incomplete evidence pack |
| Escalate | RED aggregate or payee mismatch |
| Officer override | Bank policy exception (logged) |

LangGraph **interrupt** / checkpoint semantics apply: graph suspends, human acts, graph resumes with audit entry.

## Audit Trail

Every node execution produces:

- `node_id` — graph node name
- `artifact_id` — deterministic ID for outputs
- `timestamp` — ISO 8601
- `inputs_hash` — hash of state slice consumed
- `decision` — outcome enum where applicable

Links to [`ATTESTATION_FORMAT.md`](ATTESTATION_FORMAT.md) for metadata-only chain attestation of Closing Passport hash.

## Runtime

**Primary:** [LangGraph.js](https://langchain-ai.github.io/langgraphjs/) — state schema, conditional edges, parallel branches, checkpointing, human-in-the-loop.

**Not core:**

- OpenClaw / Hermes — self-hosted execution agents; wrong trust model for bank settlement
- CRAB — research benchmark for multimodal agents; not product runtime
- MCP / A2A — future policy-controlled tool infra; not MVP orchestration core

See [`AGENT_STACK_EVALUATION.md`](AGENT_STACK_EVALUATION.md) for full framework filter.

## Relationship to Buyer Consultation Agent

| Layer | Role |
|-------|------|
| [Buyer Consultation Agent](BUYER_CONSULTATION_AGENT.md) | Nonlinear discovery/education; calls bank APIs as tools |
| Bank decision graph (this doc) | Deterministic rules + scored branches; settlement authority |

The consultation agent **does not** replace Property Shield or Risk Aggregator. It prepares the buyer and invokes bank-grade nodes when ready.

## Pitch Lines

**EN:**

> The system explores multiple settlement branches, scores each route by cost, compliance, FET-readiness, buyer protection, and bank revenue, then generates a verified closing path with escrow conditions and audit evidence.

**RU:**

> Система исследует несколько веток расчёта, оценивает каждый маршрут по стоимости, комплаенсу, FET, защите покупателя и доходу банка — и выдаёт bankable path с escrow и Closing Passport.

## Related

- [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) — buyer-facing nonlinear layer
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — system components
- [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md) — branch inputs (eight scenarios)
- [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) — local runtime for graph LLM nodes
