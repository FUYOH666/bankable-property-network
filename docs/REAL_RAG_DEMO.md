# Real RAG Demo

## Local contour

For full local stack startup (Qdrant Docker, BGE services, optional LM Studio), see [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md). For demo vs enterprise AI tiers, see [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

LM Studio (`LOCAL_AI_LLM_INSTRUCT_BASE_URL`, default `http://localhost:1234/v1`) is the optional explainability layer for schema-bound LLM output — **not invoked** in the current RAG retrieve path.

## Purpose

The real RAG demo proves that Bankable Property Network can use a controlled AI evidence pipeline instead of relying on a hardcoded story.

The flow:

1. Collect synthetic documents from `data/synthetic`.
2. Embed documents with the local BGE-M3 embedding service.
3. Store vectors in Qdrant.
4. Search by scenario context.
5. Rerank retrieved evidence with the local BGE reranker service.
6. Return retrieved evidence, scores, excerpts, and trace in the Scenario Simulator.

## Services

Required for live RAG mode:

- Qdrant at `QDRANT_URL`, default `http://localhost:6333`.
- Embedding service at `LOCAL_AI_EMBEDDING_BASE_URL`.
- Reranker service at `LOCAL_AI_RERANKER_BASE_URL`.

The API has an explicit fallback mode. If live services are unavailable in `auto` mode, it returns `retrieval_mode: deterministic_fallback` with a fallback reason.

## Commands

Start Qdrant:

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
```

Check RAG config:

```bash
curl http://localhost:8080/api/rag/health
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

Run deterministic fallback scenario:

```bash
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run?mode=fallback"
```

## Demo Interpretation

- `qdrant_embedding_reranker`: evidence was retrieved from Qdrant using embeddings and reranked.
- `deterministic_fallback`: explicit local fallback was used, usually because Qdrant or AI services were unavailable.

Both modes are explainable and safe for the demo. Live mode is stronger for showing infrastructure maturity.
