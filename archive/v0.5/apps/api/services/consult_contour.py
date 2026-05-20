"""Health checks for full local AI contour (Qdrant, BGE, LM Studio)."""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from app.services.consult_knowledge import knowledge_health

logger = logging.getLogger(__name__)


def _ping(url: str, path: str, timeout: float = 5.0) -> tuple[bool, str]:
    if not url:
        return False, "not_configured"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(f"{url.rstrip('/')}{path}")
            if response.status_code < 500:
                return True, f"ok_{response.status_code}"
            return False, f"http_{response.status_code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}"


def contour_health() -> dict[str, Any]:
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    embedding_url = os.getenv("LOCAL_AI_EMBEDDING_BASE_URL", "http://localhost:9001")
    reranker_url = os.getenv("LOCAL_AI_RERANKER_BASE_URL", "http://localhost:9002")
    llm_url = os.getenv("LOCAL_AI_LLM_INSTRUCT_BASE_URL", "").strip()

    qdrant_ok, qdrant_detail = _ping(qdrant_url, "/collections")
    embed_ok, embed_detail = _ping(embedding_url, "/healthz")
    if not embed_ok:
        embed_ok, embed_detail = _ping(embedding_url, "/livez")
    rerank_ok, rerank_detail = _ping(reranker_url, "/healthz")
    if not rerank_ok:
        rerank_ok, rerank_detail = _ping(reranker_url, "/livez")
    llm_ok, llm_detail = (False, "not_configured")
    if llm_url:
        llm_ok, llm_detail = _ping(llm_url, "/models")

    kb = knowledge_health()
    services = {
        "qdrant": {"ready": qdrant_ok, "detail": qdrant_detail, "url_env": "QDRANT_URL"},
        "embedding": {"ready": embed_ok, "detail": embed_detail, "url_env": "LOCAL_AI_EMBEDDING_BASE_URL"},
        "reranker": {"ready": rerank_ok, "detail": rerank_detail, "url_env": "LOCAL_AI_RERANKER_BASE_URL"},
        "llm_instruct": {"ready": llm_ok, "detail": llm_detail, "url_env": "LOCAL_AI_LLM_INSTRUCT_BASE_URL"},
        "knowledge_corpus": {
            "ready": kb["chunk_count"] > 0,
            "detail": f"{kb['document_count']} docs, {kb['chunk_count']} chunks",
        },
    }
    all_ready = all(s["ready"] for s in services.values())
    recommended: list[str] = []
    if not qdrant_ok:
        recommended.append("Start Qdrant: docker compose -f infra/docker-compose.yml up -d qdrant")
    if not embed_ok or not rerank_ok:
        recommended.append("Start BGE embedding :9001 and reranker :9002 on host")
    if not llm_ok:
        recommended.append("Start LM Studio local server on :1234 and set LOCAL_AI_LLM_INSTRUCT_BASE_URL")
    if qdrant_ok and embed_ok and rerank_ok:
        recommended.append("Run ingest: curl -X POST http://localhost:8080/api/rag/ingest")

    return {
        "status": "ok" if all_ready else "degraded",
        "module": "consult_contour",
        "consult_retrieval_mode": os.getenv("CONSULT_RETRIEVAL_MODE", "auto"),
        "all_ready": all_ready,
        "services": services,
        "recommended_action": recommended,
    }
