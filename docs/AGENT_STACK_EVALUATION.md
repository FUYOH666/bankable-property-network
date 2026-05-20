# Agent Stack Evaluation

Evaluation of agent frameworks and patterns for Bankable Property OS — filtered for **bank-grade decision workflow**, not hackathon speed.

Primary customer: banking anchor and regulated structures. Buyer consultation is a discovery layer; settlement authority stays deterministic.

## Verdict Summary

| Framework / Pattern | Verdict | Use in Bankable |
|---------------------|---------|-----------------|
| **LangGraph.js** | **Primary** | Nonlinear buyer consultation + settlement decision graph |
| Mastra | Secondary | Fast TS prototype; suspend/resume; not primary for bank graph |
| LlamaIndex Workflows | Document node only | SPA/FET document extraction pipeline (future) |
| OpenAI Agents SDK | Enterprise reference | RFP alignment; skip wiring unless boilerplate exists |
| Google ADK | Enterprise reference | Multi-agent orchestration story for pilots |
| AG-UI | UI pattern | Stream node status to frontend; subset without full protocol |
| MCP / A2A | Future infra | Policy-controlled tool access at scale; security review required |
| OpenClaw | **Reject as core** | Shell/browser execution — wrong trust model |
| Hermes (Nous CLI) | **Reject as core** | Dev/research agent — not settlement runtime |
| CRAB benchmark | **Reject as core** | Research multimodal benchmark — not product |

## LangGraph.js — Primary

**Why:** Official graph model with state, nodes, conditional routing, parallel execution, checkpointing, and human-in-the-loop interrupts — matches Property Shield → Capital Map → Settlement Branch Explorer → Aggregator → Escrow → Closing Passport.

**Applies to:**

- [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) — bank settlement graph
- [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) — buyer-facing nonlinear consultation

**Minimal dependency sketch (future `apps/buyer-agent/`):**

```bash
pnpm add @langchain/langgraph zod ai
# OpenAI-compatible client → LM Studio http://localhost:1234/v1 (demo)
# Production → vLLM gateway per AI_SERVICE_TIERS.md
```

**References:** [LangGraph.js Graph API](https://langchain-ai.github.io/langgraphjs/)

## Mastra — Secondary

TypeScript-first workflows with suspend/resume and visual execution graphs. Strong fit for **rapid UI demo** adjacent to Next.js.

**Use when:** prototyping buyer chat UX before committing full settlement graph to LangGraph.

**Do not use as:** sole orchestration for bank settlement authority — less explicit control over parallel branch scoring and compliance interrupts.

**References:** [Mastra Workflows](https://mastra.ai/workflows)

## LlamaIndex Workflows — Document Node Only

Event-driven pipelines for RAG, extraction, and document agents. Good for **heavy-document nodes**:

- SPA clause extraction
- FET instruction parsing
- Developer due diligence file ingestion

Not the orchestration core. Embed as a **node** inside LangGraph, not as the top-level runtime.

## OpenAI Agents SDK / Google ADK — Enterprise Reference

Useful for **RFP and pilot conversations** — tools, handoffs, guardrails, tracing, multi-agent deployment.

Skip for initial implementation unless a bank partner mandates a specific SDK. Bankable's differentiation is the **settlement graph domain model**, not the vendor agent wrapper.

## AG-UI — UI Pattern

Agent User Interaction Protocol — event stream between agent backend and frontend (tool calls, state updates, progress).

**Implement subset:** SSE or WebSocket events for node status lines in the demo UI. Full AG-UI adoption is optional post-pilot.

**References:** [AG-UI Overview](https://docs.ag-ui.com/)

## MCP / A2A — Future Infrastructure

Model Context Protocol — standard for tools/resources/prompts. Agent-to-Agent — cross-vendor agent messaging.

**Bankable stance:** **policy-controlled tool access**, not «connect everything». MCP has known security exposure in open marketplaces — whitelist tools, audit calls, no arbitrary server install in bank boundary.

Document as Phase 2 infra in production roadmap; not hackathon MVP.

## Rejected as Core

### OpenClaw / Hermes

Self-hosted agents with filesystem, browser, and shell access. Appropriate for dev automation; **inappropriate** as settlement runtime where audit, least-privilege, and deterministic gates are mandatory.

### CRAB

Cross-environment agent benchmark for evaluating multimodal agents. Research value only.

## Recommended Full Stack (Product Direction)

```text
Next.js          — demo UI + future agent chat panel
TypeScript       — buyer-agent service
LangGraph.js     — nonlinear orchestration (primary)
Zod              — state and tool I/O schemas
FastAPI          — deterministic rules engine + tool endpoints
BGE + Qdrant     — evidence retrieval (local contour)
LM Studio → vLLM — LLM tier (see AI_SERVICE_TIERS.md)
```

## Pitch One-Liners

**EN (investors who understand the product):**

> We are not building another property chatbot. We are building a nonlinear decision graph that explores settlement branches, scores them against bank and compliance dimensions, and produces auditable Closing Passport evidence — with a separate buyer consultation layer for non-linear discovery.

**RU:**

> Мы не делаем чатбот по недвижимости. Мы строим нелинейный decision graph: параллельные ветки расчёта, scoring по комплаенсу и FET, human gates и Closing Passport — плюс buyer consultation agent для нелинейного поведения пользователя. Всё в controlled local contour, на scale — vLLM и Qwen-class embeddings.

## Related

- [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md)
- [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md)
- [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md)
- [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md)
