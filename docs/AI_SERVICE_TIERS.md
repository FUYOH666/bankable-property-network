# AI Service Tiers — Demo vs Enterprise

Bankable Property OS uses AI as an **operational scaling layer** for evidence retrieval and explainability — not for autonomous money-movement decisions.

This document separates **hackathon / local demo** stack from **production / enterprise** requirements.

## Summary matrix

| Component | Demo / local (hackathon) | Enterprise / scale |
|-----------|--------------------------|---------------------|
| **LLM instruct** | LM Studio (`localhost:1234/v1`) — single user, no SLA | **vLLM** (or equivalent) behind gateway — continuous batching, multi-GPU, auth, observability |
| **Embeddings** | **BAAI/bge-m3** on MacBook MPS (`:9001`) | **Qwen3-Embedding** / Qwen-class dense (or enterprise embedding API) — higher quality at volume, multilingual TH/EN |
| **Reranker** | **bge-reranker-v2-m3** local (`:9002`) | Dedicated rerank cluster / cross-encoder on GPU pool |
| **Vector DB** | Qdrant Docker (`:6333`) | Managed Qdrant / hybrid search with SLA |
| **Fallback** | Explicit `deterministic_fallback` | Same policy — never silent degradation |
| **Decision engine** | Deterministic rules (always) | Deterministic rules + human compliance gate (always) |
| **Agent orchestration** | LangGraph.js local (`apps/buyer-agent`) | Managed graph runtime, checkpoint store, audit export |

## LLM tier

### Demo: LM Studio

- OpenAI-compatible local API on MacBook.
- Suitable for: schema-bound compliance memo drafts, counter-offer explainability, **Buyer Consultation Agent** (LangGraph.js).
- Limits: single concurrent user, no HA, model loaded in desktop app, not bank-grade SLA.

### Production: vLLM

For a **large client** or **high user concurrency**, LLM inference must run on a **vLLM** (or comparable) serving layer:

- Continuous batching and GPU pooling
- OpenAI-compatible gateway with auth and rate limits
- Model versioning and `n_ctx` governance
- Audit logs for prompts/responses (within bank boundary)

**Do not** point production traffic at LM Studio.

Env placeholder (production):

```bash
# LOCAL_AI_LLM_INSTRUCT_BASE_URL=https://your-vllm-gateway.example/v1
```

## Embedding tier

### Demo: BGE-M3

- Model: `BAAI/bge-m3`
- Runs locally on Apple Silicon (MPS) or CPU
- Supports dense + sparse + ColBERT vectors — good for hackathon corpus (~30 synthetic docs)
- Lightweight enough for demo laptop contour

### Production: Qwen-class embeddings

For **commercial RAG quality** at scale, evaluate **Qwen3-Embedding** or the latest Qwen embedding family:

- Stronger multilingual retrieval (Thai/English policy + developer docs)
- Better recall on long compliance documents
- Dimension and cost tradeoffs vs BGE-M3 — benchmark on your corpus before bank pilot

**Recommendation:** keep BGE-M3 for hackathon; plan Qwen-class (or enterprise embedding API) for 6-week bank pilot ingestion.

Env placeholder (production):

```bash
# LOCAL_AI_EMBEDDING_BASE_URL=https://your-qwen-embedding.example
```

## Reranker tier

### Demo

- `BAAI/bge-reranker-v2-m3` co-located with embedding service on MacBook.

### Production

- Dedicated rerank service with horizontal scaling
- Latency SLO per compliance review session
- Model upgrade path independent of embedding tier

## Vector store tier

### Demo

- Single Qdrant container via `infra/docker-compose.yml`
- Collection: `bankable_property_network`

### Production

- Managed Qdrant or bank-hosted vector store
- Collection per tenant (developer/bank sandbox)
- Backup, replication, access control

## Policy statement (for judges and RFPs)

> For a large number of users and bank-grade SLA, inference must run on **vLLM** (or equivalent production serving), not desktop LM Studio. Embeddings for commercial volume should use a tier above BGE-M3 — **Qwen-class embeddings** or an enterprise embedding service — evaluated on the bank's policy and developer corpus.

Money-movement **approve/reject/escalate** remains deterministic + human-in-loop regardless of AI tier.

## Code references

| Concern | Location |
|---------|----------|
| RAG retrieve path | `apps/api/src/app/services/rag.py` |
| Health + tier metadata | `GET /api/rag/health` |
| Env template | `.env.example` |
| Local runbook | [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) |

## Related

- [`MONEY_INFRASTRUCTURE_THESIS.md`](MONEY_INFRASTRUCTURE_THESIS.md) — AI as operational layer
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — controlled environment thesis
- [`REAL_RAG_DEMO.md`](REAL_RAG_DEMO.md) — ingest and scenario commands
