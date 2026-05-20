"""Lightweight demo knowledge retrieval — markdown chunks, no Qdrant."""

from __future__ import annotations

import logging
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.paths import repo_root

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = repo_root() / "data" / "consult_knowledge" / "realestate-demo"

KEYWORD_BOOSTS: dict[str, float] = {
    "price": 2.0,
    "cost": 2.0,
    "цена": 2.0,
    "стоимость": 2.0,
    "fet": 2.5,
    "freehold": 2.0,
    "leasehold": 2.0,
    "visa": 2.0,
    "виза": 2.0,
    "roi": 2.0,
    "invest": 1.5,
    "инвест": 1.5,
    "layout": 1.5,
    "планиров": 1.5,
    "payment": 1.5,
    "оплат": 1.5,
    "installment": 1.5,
    "рассроч": 1.5,
    "location": 1.5,
    "локац": 1.5,
    "квартир": 2.0,
    "apartment": 2.0,
    "unit": 1.5,
    "villa": 2.0,
    "вилл": 2.0,
    "buy": 1.5,
    "where": 1.5,
    "have": 1.0,
    "layout": 2.0,
    "landmark": 2.0,
    "sukhumvit": 2.0,
    "bangkok": 2.0,
    "сколько": 1.5,
    "стоит": 1.5,
}


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower()) if len(t) > 1}


def _split_markdown(doc_id: str, content: str) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    sections = re.split(r"(?m)^##\s+", content)
    if len(sections) <= 1:
        chunks.append({"doc_id": doc_id, "title": doc_id, "text": content.strip()[:1200]})
        return chunks
    preamble = sections[0].strip()
    if preamble:
        chunks.append({"doc_id": doc_id, "title": f"{doc_id} (intro)", "text": preamble[:1200]})
    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue
        chunks.append({"doc_id": doc_id, "title": title, "text": body[:1200]})
    return chunks


@lru_cache(maxsize=1)
def load_knowledge_corpus() -> tuple[list[dict[str, str]], list[str]]:
    chunks: list[dict[str, str]] = []
    doc_ids: list[str] = []
    if not KNOWLEDGE_DIR.is_dir():
        logger.warning("Consult knowledge dir missing: %s", KNOWLEDGE_DIR)
        return chunks, doc_ids
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        if path.name == "DEMO_NOTICE.md":
            continue
        content = path.read_text(encoding="utf-8")
        doc_id = path.name
        doc_ids.append(doc_id)
        chunks.extend(_split_markdown(doc_id, content))
    logger.info("Loaded consult knowledge: %d docs, %d chunks", len(doc_ids), len(chunks))
    return chunks, doc_ids


def _score_chunk(query_tokens: set[str], query_lower: str, chunk: dict[str, str]) -> float:
    haystack = f"{chunk['title']} {chunk['text']}".lower()
    chunk_tokens = _tokenize(haystack)
    overlap = len(query_tokens & chunk_tokens)
    if overlap == 0:
        return 0.0
    score = float(overlap)
    for keyword, boost in KEYWORD_BOOSTS.items():
        if keyword in query_lower and keyword in haystack:
            score += boost
    return score


def search_knowledge(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    chunks, _ = load_knowledge_corpus()
    if not chunks or not query.strip():
        return []
    query_lower = query.lower()
    query_tokens = _tokenize(query)
    scored: list[tuple[float, dict[str, str]]] = []
    for chunk in chunks:
        score = _score_chunk(query_tokens, query_lower, chunk)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    results: list[dict[str, Any]] = []
    for score, chunk in scored[:top_k]:
        excerpt = chunk["text"]
        if len(excerpt) > 400:
            excerpt = excerpt[:397] + "..."
        results.append(
            {
                "doc_id": chunk["doc_id"],
                "title": chunk["title"],
                "excerpt": excerpt,
                "score": round(score, 2),
            }
        )
    return results


def knowledge_health() -> dict[str, Any]:
    chunks, doc_ids = load_knowledge_corpus()
    return {
        "status": "ok",
        "module": "consult_knowledge",
        "corpus_path": str(KNOWLEDGE_DIR.relative_to(repo_root())),
        "document_count": len(doc_ids),
        "chunk_count": len(chunks),
        "retrieval_mode": "keyword_chunk_search",
    }
