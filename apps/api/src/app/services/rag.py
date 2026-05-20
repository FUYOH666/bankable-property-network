"""RAG evidence pipeline for Bankable Property OS.

Demo stack: Qdrant + BGE-M3 embedding + BGE reranker (local MacBook contour).
Production tier: vLLM gateway + Qwen-class embeddings — see docs/AI_SERVICE_TIERS.md.
LLM instruct is not invoked in the retrieve path today; generation is roadmap.
"""

import hashlib
import os
import re
import uuid
from pathlib import Path
from typing import Any

import httpx

from app.services.scenarios import get_scenario_detail, run_scenario


from app.paths import synthetic_root
DEFAULT_COLLECTION = "bankable_property_network"
SUPPORTED_SUFFIXES = {".md", ".json"}


def _settings() -> dict[str, str]:
    return {
        "qdrant_url": os.getenv("QDRANT_URL", "http://localhost:6333"),
        "embedding_url": os.getenv("LOCAL_AI_EMBEDDING_BASE_URL", "http://localhost:9001"),
        "reranker_url": os.getenv("LOCAL_AI_RERANKER_BASE_URL", "http://localhost:9002"),
        "collection": os.getenv("QDRANT_COLLECTION", DEFAULT_COLLECTION),
    }


def collect_synthetic_documents() -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    for path in sorted(synthetic_root().rglob("*")):
        if not path.is_file() or path.suffix not in SUPPORTED_SUFFIXES:
            continue
        relative_path = path.relative_to(synthetic_root()).as_posix()
        text = path.read_text(encoding="utf-8")
        documents.append(
            {
                "id": relative_path,
                "kind": relative_path.split("/", maxsplit=1)[0],
                "text": text,
                "source_path": f"data/synthetic/{relative_path}",
            }
        )
    return documents


def rag_health() -> dict[str, Any]:
    settings = _settings()
    deployment_tier = os.getenv("BANKABLE_AI_TIER", "demo_local")
    return {
        "collection": settings["collection"],
        "qdrant_url_configured": bool(settings["qdrant_url"]),
        "embedding_url_configured": bool(settings["embedding_url"]),
        "reranker_url_configured": bool(settings["reranker_url"]),
        "synthetic_document_count": len(collect_synthetic_documents()),
        "deployment_tier": deployment_tier,
        "embedding_tier": "bge-m3",
        "llm_tier": "lm_studio_optional",
        "production_note": (
            "For scale use vLLM + Qwen-class embeddings — see docs/AI_SERVICE_TIERS.md"
        ),
    }


def _embed(texts: list[str], timeout: float = 30) -> list[list[float]]:
    settings = _settings()
    with httpx.Client(timeout=timeout) as client:
        response = client.post(
            f"{settings['embedding_url']}/v1/embeddings",
            json={"input": texts, "return_dense": True, "return_sparse": False, "return_colbert": False},
        )
        response.raise_for_status()
    data = response.json()["data"]
    return [item["dense_embedding"] for item in data]


def _point_id(document_id: str) -> str:
    digest = hashlib.sha256(document_id.encode("utf-8")).hexdigest()
    return str(uuid.UUID(digest[:32]))


def ingest_synthetic_documents(dry_run: bool = False) -> dict[str, Any]:
    documents = collect_synthetic_documents()
    if dry_run:
        return {"mode": "dry_run", "document_count": len(documents), "collection": _settings()["collection"]}

    if not documents:
        return {"mode": "live", "document_count": 0, "collection": _settings()["collection"], "status": "empty"}

    settings = _settings()
    vectors = _embed([doc["text"] for doc in documents])
    vector_size = len(vectors[0])
    points = [
        {
            "id": _point_id(doc["id"]),
            "vector": vector,
            "payload": doc,
        }
        for doc, vector in zip(documents, vectors, strict=True)
    ]

    with httpx.Client(timeout=60) as client:
        collection_response = client.put(
            f"{settings['qdrant_url']}/collections/{settings['collection']}",
            json={"vectors": {"size": vector_size, "distance": "Cosine"}},
        )
        if collection_response.status_code != 409:
            collection_response.raise_for_status()
        upsert_response = client.put(
            f"{settings['qdrant_url']}/collections/{settings['collection']}/points",
            params={"wait": "true"},
            json={"points": points},
        )
        upsert_response.raise_for_status()

    return {
        "mode": "live",
        "document_count": len(documents),
        "collection": settings["collection"],
        "vector_size": vector_size,
        "status": "indexed",
    }


def _scenario_query(detail: dict[str, Any]) -> str:
    return " ".join(
        [
            detail["id"],
            detail["capital_status"],
            detail["property_status"],
            detail["agent_status"],
            detail["route_decision"],
            detail["buyer"]["profile"],
            detail["project"]["name"],
            detail["project"]["notes"],
            detail["agent"]["status"],
        ]
    )


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(token) > 2}


def _fallback_retrieve(query: str, limit: int = 6) -> list[dict[str, Any]]:
    query_tokens = _tokenize(query)
    scored: list[dict[str, Any]] = []
    for doc in collect_synthetic_documents():
        doc_id = doc["id"].lower()
        doc_tokens = _tokenize(f"{doc['id']} {doc['text']}")
        overlap = query_tokens & doc_tokens
        if not overlap:
            score = 0.0
        else:
            score = len(overlap) / max(len(query_tokens), 1)
        for keyword in ["swift", "usdt", "cash", "p2p", "fet", "payment", "agent", "developer"]:
            if keyword in query.lower() and keyword in doc_id:
                score += 0.5
        scored.append(
            {
                "document_id": doc["id"],
                "kind": doc["kind"],
                "score": round(score, 4),
                "rerank_score": None,
                "excerpt": doc["text"][:360].replace("\n", " "),
                "source_path": doc["source_path"],
            }
        )
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]


def _qdrant_search(query: str, limit: int = 8) -> list[dict[str, Any]]:
    settings = _settings()
    query_vector = _embed([query])[0]
    with httpx.Client(timeout=30) as client:
        response = client.post(
            f"{settings['qdrant_url']}/collections/{settings['collection']}/points/search",
            json={"vector": query_vector, "limit": limit, "with_payload": True},
        )
        response.raise_for_status()
    points = response.json().get("result") or response.json().get("points") or []
    return [
        {
            "document_id": point["payload"]["id"],
            "kind": point["payload"]["kind"],
            "score": round(float(point.get("score", 0.0)), 4),
            "rerank_score": None,
            "excerpt": point["payload"]["text"][:360].replace("\n", " "),
            "source_path": point["payload"]["source_path"],
            "text": point["payload"]["text"],
        }
        for point in points
    ]


def _rerank(query: str, evidence: list[dict[str, Any]], limit: int = 6) -> list[dict[str, Any]]:
    if not evidence:
        return []
    settings = _settings()
    documents = [item["text"] for item in evidence]
    with httpx.Client(timeout=30) as client:
        response = client.post(
            f"{settings['reranker_url']}/v1/rerank",
            json={"query": query, "documents": documents, "top_n": min(limit, len(documents)), "normalize": True},
        )
        response.raise_for_status()
    results = response.json().get("results", [])

    reranked: list[dict[str, Any]] = []
    for result in results:
        index = result.get("index")
        if index is None and "document" in result:
            try:
                index = documents.index(result["document"])
            except ValueError:
                index = 0
        item = dict(evidence[int(index)])
        item.pop("text", None)
        item["rerank_score"] = round(float(result.get("relevance_score", result.get("score", 0.0))), 4)
        reranked.append(item)
    return reranked


def retrieve_evidence(query: str, mode: str = "auto", limit: int = 6) -> tuple[str, list[dict[str, Any]], str | None]:
    if mode == "fallback":
        return "deterministic_fallback", _fallback_retrieve(query, limit=limit), None

    try:
        evidence = _qdrant_search(query, limit=max(limit, 8))
        reranked = _rerank(query, evidence, limit=limit)
        return "qdrant_embedding_reranker", reranked or evidence[:limit], None
    except Exception as exc:
        if mode == "live":
            raise
        return "deterministic_fallback", _fallback_retrieve(query, limit=limit), f"{type(exc).__name__}: {exc}"


def run_scenario_with_rag(scenario_id: str, mode: str = "auto") -> dict[str, Any] | None:
    scenario_result = run_scenario(scenario_id)
    detail = get_scenario_detail(scenario_id)
    if scenario_result is None or detail is None:
        return None

    query = _scenario_query(detail)
    retrieval_mode, evidence, fallback_reason = retrieve_evidence(query, mode=mode)
    scenario_result["retrieval_mode"] = retrieval_mode
    scenario_result["retrieval_fallback_reason"] = fallback_reason
    scenario_result["retrieved_evidence"] = evidence
    scenario_result["rag_trace"] = [
        {
            "kind": "retrieved_evidence",
            "document_id": item["document_id"],
            "reason": f"Retrieved via {retrieval_mode} with score {item['rerank_score'] if item['rerank_score'] is not None else item['score']}.",
        }
        for item in evidence
    ]
    return scenario_result
