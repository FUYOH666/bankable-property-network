from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz_reports_ready_service() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_demo_endpoint_returns_closing_passport_flow() -> None:
    response = client.get("/api/demo/closing-passport")

    assert response.status_code == 200
    body = response.json()
    assert body["case"]["id"] == "case-anchor-deposit-mismatch"
    assert body["case"]["network_positioning"] == "bankable_property_network"
    assert any(source["id"] == "src-bank-dubai" for source in body["case"]["capital_sources"])
    assert body["property_shield"]["risk_level"] == "high"
    assert body["recommended_route"]["id"] == "bankable_escrow"
    assert "FET-ready" in body["bank_counter_offer"]["product"]
    assert body["closing_passport"]["attestation"]["settlement_route_approved"] is True


def test_demo_endpoint_allows_local_frontend_cors() -> None:
    response = client.options(
        "/api/demo/closing-passport",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_demo_endpoint_allows_scanovich_production_cors() -> None:
    response = client.options(
        "/api/demo/closing-passport",
        headers={
            "Origin": "https://scanovich.ai",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://scanovich.ai"


def test_closing_passport_includes_infrastructure_context() -> None:
    response = client.get("/api/demo/closing-passport")

    assert response.status_code == 200
    context = response.json()["infrastructure_context"]
    assert context["failure_mode"] == "unverified_settlement_path"
    assert context["root_cause"] == "developer_paid_commissions_no_entry_barrier"
    assert context["primary_customer"] == "banking_anchor"


def test_evidence_pack_endpoint_returns_exportable_privacy_safe_json() -> None:
    response = client.get("/api/demo/evidence-pack")

    assert response.status_code == 200
    body = response.json()
    assert body["data_classification"] == "synthetic_demo_data"
    assert body["export_type"] == "closing_passport_evidence_pack"
    assert body["evidence_pack_hash"].startswith("0x")
    assert "passport_number" not in str(body)
    assert "bank_statement_raw" not in str(body)


def test_scenario_api_lists_synthetic_scenarios() -> None:
    response = client.get("/api/scenarios")

    assert response.status_code == 200
    body = response.json()
    scenario_ids = [scenario["id"] for scenario in body["scenarios"]]
    assert "swift-clean-route" in scenario_ids
    assert "usdt-mixed-route" in scenario_ids
    assert "cash-red-route" in scenario_ids


def test_scenario_api_returns_scenario_detail() -> None:
    response = client.get("/api/scenarios/developer-suspicious-route")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "developer-suspicious-route"
    assert body["project"]["risk_level"] == "amber"
    assert body["buyer"]["expected_status"] == "green"


def test_scenario_runner_classifies_green_amber_red_and_property_risk() -> None:
    green = client.get("/api/scenarios/swift-clean-route/run").json()
    amber = client.get("/api/scenarios/usdt-mixed-route/run").json()
    red = client.get("/api/scenarios/cash-red-route/run").json()
    property_risk = client.get("/api/scenarios/developer-suspicious-route/run").json()

    assert green["capital_status"] == "green"
    assert green["bank_action"] == "approve"
    assert green["closing_passport_status"] == "generated"

    assert amber["capital_status"] == "amber"
    assert amber["bank_action"] == "conditional_approve"

    assert red["capital_status"] == "red"
    assert red["bank_action"] in {"reject", "escalate"}
    assert red["closing_passport_status"] == "not_generated"

    assert property_risk["property_risk"] == "high"
    assert property_risk["bank_action"] == "escalate"
    assert property_risk["route_decision"] == "block_until_payee_authority"


def test_scenario_runner_returns_rag_trace_and_privacy_safe_evidence() -> None:
    response = client.get("/api/scenarios/swift-clean-route/run")

    assert response.status_code == 200
    body = response.json()
    trace_kinds = {item["kind"] for item in body["rag_trace"]}
    assert {"policy", "developer_profile", "agent_profile", "payment_instruction", "route_rule", "compliance_memo"} <= trace_kinds
    assert body["evidence_preview"]["excluded_sensitive_fields"] == ["passport_number", "email", "phone", "address", "full_name"]
    assert "SHOULD-NOT-LEAK" not in str(body)
    assert "bank_statement_raw" not in str(body)


def test_developer_knowledge_hub_detects_payee_mismatch() -> None:
    response = client.get("/api/demo/developer-knowledge-hub")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "developer_knowledge_hub"
    assert body["knowledge_vs_agent_gap"]["status"] == "mismatch_detected"
    assert body["knowledge_vs_agent_gap"]["developer_authorized_payee"] == "Siam Riverside Living Co., Ltd."
    assert body["knowledge_vs_agent_gap"]["agent_claimed_payee"] == "SRL Holding 2026 Co., Ltd."
    assert body["source_of_truth"] == "developer_erp_feed"
    assert len(body["channel_roadmap"]) == 5
    channels = {item["id"]: item["status"] for item in body["channel_roadmap"]}
    assert channels["web"] == "live"
    assert channels["whatsapp"] == "live"
    assert channels["telegram"] == "roadmap"


def test_developer_knowledge_hub_includes_prior_art_reference() -> None:
    response = client.get("/api/demo/developer-knowledge-hub")

    assert response.status_code == 200
    body = response.json()
    assert "github.com" in body["prior_art"]["reference_url"]
    assert body["consumption_model"] == "verified_agencies_read_only_from_hub"


def test_scenario_detail_returns_404_for_unknown_id() -> None:
    response = client.get("/api/scenarios/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Scenario not found"


def test_scenario_run_returns_404_for_unknown_id() -> None:
    response = client.get("/api/scenarios/does-not-exist/run")

    assert response.status_code == 404


def test_scenario_rag_run_returns_404_for_unknown_id() -> None:
    response = client.get("/api/scenarios/does-not-exist/rag-run")

    assert response.status_code == 404
