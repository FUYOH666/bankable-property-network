from app.services.consult_knowledge import knowledge_health, load_knowledge_corpus, search_knowledge


def test_knowledge_corpus_loads() -> None:
    chunks, doc_ids = load_knowledge_corpus()
    assert len(doc_ids) >= 5
    assert len(chunks) >= 10


def test_knowledge_health_reports_counts() -> None:
    health = knowledge_health()
    assert health["status"] == "ok"
    assert health["document_count"] >= 5
    assert health["chunk_count"] >= 10


def test_search_knowledge_fet_query() -> None:
    hits = search_knowledge("FET requirements foreign buyer", top_k=2)
    assert hits
    assert any("FET" in hit["excerpt"] or "fet" in hit["excerpt"].lower() for hit in hits)


def test_search_knowledge_price_russian() -> None:
    hits = search_knowledge("сколько стоит квартира", top_k=2)
    assert hits
    assert hits[0]["doc_id"].endswith(".md")
