from fastapi.testclient import TestClient

from app.main import app
from app.services.rag import collect_consult_kb_documents, collect_synthetic_documents


client = TestClient(app)


def test_collect_synthetic_documents_includes_professional_evidence_docs() -> None:
    docs = collect_synthetic_documents()
    doc_ids = {doc["id"] for doc in docs}

    assert "documents/swift_bank_statement_summary.md" in doc_ids
    assert "documents/usdt_wallet_summary.md" in doc_ids
    assert "documents/cash_p2p_declaration.md" in doc_ids
    assert "policies/property_settlement_policy.md" in doc_ids


def test_rag_health_reports_configuration_without_external_dependency() -> None:
    response = client.get("/api/rag/health")

    assert response.status_code == 200
    body = response.json()
    assert body["collection"] == "bankable_property_network"
    assert "qdrant_url_configured" in body
    assert "embedding_url_configured" in body
    assert "reranker_url_configured" in body
    assert body["deployment_tier"] == "demo_local"
    assert body["embedding_tier"] == "bge-m3"
    assert body["llm_tier"] == "lm_studio_optional"
    assert "AI_SERVICE_TIERS.md" in body["production_note"]


def test_rag_ingest_dry_run_counts_synthetic_documents() -> None:
    response = client.post("/api/rag/ingest?dry_run=true")

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "dry_run"
    assert body["document_count"] >= 10
    assert body["consult_kb_document_count"] == len(collect_consult_kb_documents())
    assert body["consult_kb_document_count"] >= 5
    assert body["document_count"] == body["synthetic_document_count"] + body["consult_kb_document_count"]


def test_scenario_rag_run_fallback_returns_traceable_evidence() -> None:
    response = client.get("/api/scenarios/usdt-mixed-route/rag-run?mode=fallback")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "usdt-mixed-route"
    assert body["retrieval_mode"] == "deterministic_fallback"
    assert len(body["retrieved_evidence"]) >= 3
    assert any("usdt" in item["document_id"] for item in body["retrieved_evidence"])
    assert body["rag_trace"][0]["kind"] == "retrieved_evidence"
