from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services import buyer_consultation as bc


client = TestClient(app)


def test_consult_healthz() -> None:
    response = client.get("/api/consult/healthz")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["module"] == "buyer_consultation"
    assert body["knowledge_corpus"]["document_count"] >= 5


def test_consult_knowledge_healthz() -> None:
    response = client.get("/api/consult/knowledge/healthz")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "consult_knowledge"
    assert body["chunk_count"] >= 10


def test_consult_greeting_ru_no_payee_mismatch() -> None:
    response = client.post(
        "/api/consult/message",
        json={"session_id": "greet-ru", "message": "Ку", "channel": "web"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "greeting"
    assert "SRL Holding" not in body["reply"]
    assert "mismatch" not in body["reply"].lower()
    assert "developer_hub_snapshot" not in body["tools_used"]


def test_consult_project_faq_cites_knowledge() -> None:
    response = client.post(
        "/api/consult/message",
        json={
            "session_id": "faq-1",
            "message": "сколько стоит квартира и FET",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] in {"project_faq", "mixed"}
    assert any(
        t in body["tools_used"] for t in ("consult_knowledge_search", "consult_rag_search")
    )
    assert body["citations"]


def test_consult_rag_citations_include_rerank_score() -> None:
    evidence = [
        {
            "document_id": "consult_kb/FAQ.md",
            "kind": "consult_kb",
            "excerpt": "Studio from 3.2M THB",
            "score": 0.9,
            "rerank_score": 0.87,
            "source_path": "data/consult_knowledge/realestate-demo/FAQ.md",
        }
    ]
    with patch(
        "app.services.consult_retrieval.retrieve_consult_evidence",
        return_value=("qdrant_embedding_reranker", evidence, None),
    ):
        response = client.post(
            "/api/consult/message",
            json={
                "session_id": "rag-faq",
                "message": "сколько стоит квартира и FET",
                "channel": "web",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert "consult_rag_search" in body["tools_used"]
    assert any(c.get("rerank_score") is not None for c in body["citations"])


def test_consult_contour_healthz() -> None:
    response = client.get("/api/consult/contour/healthz")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "consult_contour"
    assert "services" in body
    assert "qdrant" in body["services"]
    assert "llm_instruct" in body["services"]
    assert "consult_retrieval_mode" in body


def test_consult_settlement_uses_hub() -> None:
    response = client.post(
        "/api/consult/message",
        json={
            "session_id": "settlement-1",
            "message": "What is the payee mismatch on escrow?",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] in {"settlement", "mixed"}
    assert "developer_hub_snapshot" in body["tools_used"]
    assert "SRL Holding" in body["reply"] or any(
        "SRL" in c.get("fact", "") for c in body["citations"]
    )


def test_llm_chat_payload_disables_thinking_for_qwen_by_default() -> None:
    with patch.dict("os.environ", {"LOCAL_AI_LLM_ENABLE_THINKING": "false"}, clear=False):
        payload = bc._llm_chat_payload([{"role": "user", "content": "hi"}])
    assert payload["chat_template_kwargs"] == {"enable_thinking": False}


def test_extract_llm_text_prefers_content_over_reasoning() -> None:
    text = bc._extract_llm_text(
        {"content": "Bangkok luxury condos.", "reasoning_content": "Here's a thinking process:\n1. ..."}
    )
    assert text == "Bangkok luxury condos."


def test_consult_message_uses_template_when_llm_unavailable() -> None:
    with patch.dict("os.environ", {"LOCAL_AI_LLM_INSTRUCT_BASE_URL": "http://127.0.0.1:59999/v1"}, clear=False):
        with patch("app.services.buyer_consultation.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__.return_value = mock_client
            mock_client.post.side_effect = ConnectionError("LLM down")
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/api/consult/message",
                json={
                    "session_id": "fallback-session",
                    "message": "Tell me about SWIFT clean route",
                    "channel": "web",
                },
            )

    assert response.status_code == 200
    body = response.json()
    assert body["retrieval_mode"] in {
        "deterministic_template",
        "keyword_template",
        "rag_template",
        "purchase_pitch_template",
    }
    assert "scenario_hint:swift-clean-route" in body["tools_used"]


def test_consult_red_route_does_not_encourage_deposit() -> None:
    response = client.post(
        "/api/consult/message",
        json={
            "session_id": "red-route-session",
            "message": "Can I deposit cash today on the cash route?",
            "channel": "web",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "scenario_hint:cash-red-route" in body["tools_used"]
    reply_lower = body["reply"].lower()
    assert "do not" in reply_lower or "rejected" in reply_lower or "не переводите" in reply_lower


def test_is_prompt_leak_detects_system_fragments() -> None:
    assert bc._is_prompt_leak("Settlement/money questions → cite bank API facts.")
    assert bc._is_prompt_leak("Project sales questions → cite bank API facts.")
    assert not bc._is_prompt_leak("Landmark Sukhumvit Tower — USDT amber route with escrow.")


def test_is_purchase_pitch_message_mixed_usdt() -> None:
    assert bc._is_purchase_pitch_message("а как покупать? у меня usdt", "mixed")
    assert not bc._is_purchase_pitch_message("сколько стоит квартира?", "project_faq")


def test_consult_usdt_purchase_pitch_no_prompt_leak() -> None:
    with patch.dict("os.environ", {"LOCAL_AI_LLM_INSTRUCT_BASE_URL": "http://127.0.0.1:59999/v1"}, clear=False):
        with patch("app.services.buyer_consultation.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__.return_value = mock_client
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "choices": [
                    {"message": {"content": "Settlement/money questions → cite bank API facts."}}
                ]
            }
            mock_client.post.return_value = mock_response
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/api/consult/message",
                json={
                    "session_id": "usdt-pitch-leak",
                    "message": "а как покупать? у меня usdt",
                    "channel": "whatsapp",
                },
            )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "mixed"
    assert "scenario_hint:usdt-mixed-route" in body["tools_used"]
    reply_lower = body["reply"].lower()
    assert "cite bank api" not in reply_lower
    assert "settlement/money questions" not in reply_lower
    assert any(
        token in reply_lower
        for token in ("usdt", "янтар", "amber", "эскроу", "escrow", "fet", "landmark")
    )
    assert body["retrieval_mode"] == "purchase_pitch_template"


def test_consult_usdt_purchase_pitch_when_llm_unavailable() -> None:
    with patch.dict("os.environ", {"LOCAL_AI_LLM_INSTRUCT_BASE_URL": "http://127.0.0.1:59999/v1"}, clear=False):
        with patch("app.services.buyer_consultation.httpx.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client.__enter__.return_value = mock_client
            mock_client.post.side_effect = ConnectionError("LLM down")
            mock_client_cls.return_value = mock_client

            response = client.post(
                "/api/consult/message",
                json={
                    "session_id": "usdt-pitch-offline",
                    "message": "а как покупать? у меня usdt",
                    "channel": "whatsapp",
                },
            )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "mixed"
    assert body["retrieval_mode"] == "purchase_pitch_template"
    assert "cite bank api" not in body["reply"].lower()
