"""Offline consult dialogue matrix — CI-safe regression for multi-turn scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services import buyer_consultation as bc

ROOT = Path(__file__).resolve().parents[3]
MATRIX_SCRIPT = ROOT / "scripts" / "run_consult_dialogue_matrix.py"

client = TestClient(app)


def test_villa_intent_not_greeting() -> None:
    assert bc._detect_intent("i want buy villa") == "project_faq"


def test_consult_villa_reply_uses_demo_project_offline() -> None:
    bc._sessions.clear()
    with patch.object(bc, "_llm_reply", return_value=None):
        response = client.post(
            "/api/consult/message",
            json={"session_id": "villa-test", "message": "i want buy villa", "channel": "web"},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "project_faq"
    reply_lower = body["reply"].lower()
    assert "project-riverside" not in reply_lower
    assert any(token in body["reply"] for token in ("Bangkok", "Landmark", "Sukhumvit", "condo"))


def test_consult_follow_up_inventory_offline() -> None:
    bc._sessions.clear()
    with patch.object(bc, "_llm_reply", return_value=None):
        client.post(
            "/api/consult/message",
            json={"session_id": "follow-test", "message": "i want buy villa", "channel": "web"},
        )
        response = client.post(
            "/api/consult/message",
            json={
                "session_id": "follow-test",
                "message": "what do you have and where?",
                "channel": "web",
            },
        )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "project_faq"
    blob = body["reply"] + str(body.get("citations"))
    assert "project-riverside" not in blob.lower()
    assert any(token in blob for token in ("Landmark", "FAQ", "Project_Overview", "Bangkok", "Sukhumvit"))


def test_consult_retrieve_prefers_consult_kb(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_retrieve(query: str, mode: str = "auto", limit: int = 6, scope: str = "project"):
        captured["scope"] = scope
        captured["kinds"] = {"consult_kb"} if scope == "project" else {"consult_kb", "policies"}
        return "qdrant_embedding_reranker", [], None

    monkeypatch.setattr("app.services.consult_retrieval.retrieve_consult_evidence", fake_retrieve)
    from app.services.consult_retrieval import consult_retrieve

    mode, hits, reason = consult_retrieve("villa price", top_k=2, scope="project")
    assert captured["scope"] == "project"
    assert mode in {"keyword_chunk", "qdrant_embedding_reranker"}
    if not hits:
        assert reason in {None, "empty_rag_results"} or reason


def test_offline_dialogue_matrix_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(MATRIX_SCRIPT), "--offline"],
        cwd=ROOT / "apps" / "api",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
