"""Consult retrieval — RAG pipeline with keyword fallback."""

from __future__ import annotations

import logging
import os
from typing import Any, Literal

from app.services.consult_knowledge import search_knowledge
from app.services.rag import retrieve_consult_evidence, retrieve_evidence

logger = logging.getLogger(__name__)

ConsultScope = Literal["project", "settlement"]


def _keyword_hits(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    return [
        {
            "document_id": hit["doc_id"],
            "kind": "consult_kb",
            "title": hit["title"],
            "excerpt": hit["excerpt"],
            "score": hit.get("score"),
            "rerank_score": None,
            "source_path": f"data/consult_knowledge/realestate-demo/{hit['doc_id']}",
        }
        for hit in search_knowledge(query, top_k=top_k)
    ]


def _evidence_to_hits(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for item in evidence:
        doc_id = item.get("document_id", "")
        hits.append(
            {
                "document_id": doc_id,
                "doc_id": doc_id.split("/")[-1] if doc_id else "",
                "kind": item.get("kind", ""),
                "title": doc_id.split("/")[-1] if doc_id else doc_id,
                "excerpt": item.get("excerpt", ""),
                "score": item.get("score"),
                "rerank_score": item.get("rerank_score"),
                "source_path": item.get("source_path", ""),
            }
        )
    return hits


def consult_retrieve(
    query: str,
    top_k: int = 3,
    scope: ConsultScope = "project",
) -> tuple[str, list[dict[str, Any]], str | None]:
    mode = os.getenv("CONSULT_RETRIEVAL_MODE", "auto").strip().lower()

    if mode == "keyword":
        hits = _keyword_hits(query, top_k=top_k)
        return "keyword_chunk", hits, None

    retrieve_fn = retrieve_consult_evidence
    retrieve_kwargs: dict[str, Any] = {"scope": scope}

    if mode == "rag":
        retrieval_mode, evidence, fallback_reason = retrieve_fn(
            query, mode="live", limit=top_k, **retrieve_kwargs
        )
        return retrieval_mode, _evidence_to_hits(evidence), fallback_reason

    retrieval_mode, evidence, fallback_reason = retrieve_fn(
        query, mode="auto", limit=top_k, **retrieve_kwargs
    )
    hits = _evidence_to_hits(evidence)
    if not hits:
        keyword_hits = _keyword_hits(query, top_k=top_k)
        if keyword_hits:
            reason = fallback_reason or "empty_rag_results"
            logger.warning("Consult RAG empty, using keyword: %s", reason)
            return "keyword_chunk", keyword_hits, reason
    if retrieval_mode == "deterministic_fallback" and fallback_reason:
        logger.warning("Consult RAG fallback to keyword: %s", fallback_reason)
        keyword_hits = _keyword_hits(query, top_k=top_k)
        if keyword_hits:
            return "keyword_chunk", keyword_hits, fallback_reason
    return retrieval_mode, hits, fallback_reason
