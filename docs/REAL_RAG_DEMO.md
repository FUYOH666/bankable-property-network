# Real RAG Demo

## Local contour

For full local stack startup (Qdrant Docker, BGE services, LM Studio), see [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md). For demo vs enterprise AI tiers, see [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

**Two RAG paths:**

1. **Scenario Simulator** — embeds/reranks `data/synthetic/` corpus; LLM optional for explainability on scenario runs.
2. **Buyer Consultation** — uses `consult_kb` filter over `data/consult_knowledge/realestate-demo/` (+ settlement policies); **LM Studio is invoked** when `LOCAL_AI_LLM_INSTRUCT_BASE_URL` is set (`rag_llm` mode). Explicit keyword/template fallback when services are down.

## Purpose

The real RAG demo proves that Bankable Property Network can use a controlled AI evidence pipeline instead of relying on a hardcoded story.

The flow:

1. Collect synthetic documents from `data/synthetic` and consult KB from `data/consult_knowledge/realestate-demo/`.
2. Embed documents with the local BGE-M3 embedding service.
3. Store vectors in Qdrant.
4. Search by scenario context or consult message (with `kind=consult_kb` filter for project FAQ).
5. Rerank retrieved evidence with the local BGE reranker service.
6. Return retrieved evidence, scores, excerpts, and trace in Scenario Simulator or consult reply.

## Services

Required for live RAG mode:

- Qdrant at `QDRANT_URL`, default `http://localhost:6333`.
- Embedding service at `LOCAL_AI_EMBEDDING_BASE_URL`.
- Reranker service at `LOCAL_AI_RERANKER_BASE_URL`.
- LM Studio at `LOCAL_AI_LLM_INSTRUCT_BASE_URL` (consult natural replies; Qwen 3.6 with `LOCAL_AI_LLM_ENABLE_THINKING=false`).

The API has an explicit fallback mode. If live services are unavailable in `auto` mode, it returns `retrieval_mode: deterministic_fallback` or `keyword_fallback` / `rag_template` with a logged reason.

## Commands

Start Qdrant:

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
```

Check RAG config:

```bash
curl http://localhost:8080/api/rag/health
curl http://localhost:8080/api/consult/contour/healthz
```

Dry-run ingestion:

```bash
curl -X POST "http://localhost:8080/api/rag/ingest?dry_run=true"
```

Live ingestion:

```bash
curl -X POST http://localhost:8080/api/rag/ingest
```

Run live/auto RAG scenario:

```bash
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run"
```

Consult message (live RAG + LLM when contour up):

```bash
curl -s -X POST http://localhost:8080/api/consult/message \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"rag-demo","channel":"web","message":"What is the price for a 2BR at Landmark Sukhumvit?"}'
```

## Demo Interpretation

- `qdrant_embedding_reranker` / `rag_llm`: evidence retrieved from Qdrant; consult may call LM Studio for natural reply.
- `rag_template` / `keyword_fallback` / `deterministic_fallback`: explicit local fallback — no silent degrade.

Both modes are explainable and safe for the demo. Live mode is stronger for showing infrastructure maturity.

## Related

- [`CONSULT_KNOWLEDGE_DEMO.md`](CONSULT_KNOWLEDGE_DEMO.md)
- [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md)
- [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md)
