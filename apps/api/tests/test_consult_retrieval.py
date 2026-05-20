from unittest.mock import patch

from app.services.consult_retrieval import consult_retrieve


def test_consult_retrieve_auto_falls_back_to_keyword_when_qdrant_raises() -> None:
    with patch.dict("os.environ", {"CONSULT_RETRIEVAL_MODE": "auto"}, clear=False):
        with patch("app.services.rag._qdrant_search", side_effect=ConnectionError("qdrant down")):
            mode, hits, fallback = consult_retrieve("FET visa price", top_k=2)

    assert mode == "keyword_chunk"
    assert fallback is not None
    assert "ConnectionError" in fallback
    assert hits
    assert hits[0]["document_id"]


def test_consult_retrieve_keyword_mode_skips_rag() -> None:
    with patch.dict("os.environ", {"CONSULT_RETRIEVAL_MODE": "keyword"}, clear=False):
        with patch("app.services.rag._qdrant_search", side_effect=AssertionError("should not call qdrant")):
            mode, hits, fallback = consult_retrieve("FET Bangkok apartment price", top_k=1)

    assert mode == "keyword_chunk"
    assert fallback is None
    assert hits


def test_consult_retrieve_rag_mode_returns_reranked_hits() -> None:
    evidence = [
        {
            "document_id": "consult_kb/FAQ.md",
            "kind": "consult_kb",
            "excerpt": "FET pricing overview",
            "score": 0.91,
            "rerank_score": 0.88,
            "source_path": "data/consult_knowledge/realestate-demo/FAQ.md",
        }
    ]
    with patch.dict("os.environ", {"CONSULT_RETRIEVAL_MODE": "rag"}, clear=False):
        with patch(
            "app.services.consult_retrieval.retrieve_consult_evidence",
            return_value=("qdrant_embedding_reranker", evidence, None),
        ):
            mode, hits, fallback = consult_retrieve("FET price", top_k=1)

    assert mode == "qdrant_embedding_reranker"
    assert fallback is None
    assert hits[0]["rerank_score"] == 0.88
