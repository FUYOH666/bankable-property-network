from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_prelaunch_off_platform_scenario_blocks_passport() -> None:
    response = client.get("/api/scenarios/prelaunch-off-platform-route/run")

    assert response.status_code == 200
    body = response.json()
    assert body["property_risk"] == "high"
    assert body["closing_passport_status"] == "not_generated"
    assert "prelaunch_without_permit" in body["supply_risk_signals"]
    assert body["route_decision"] == "reject_prelaunch_no_permit"


def test_tier_one_landmark_scenario_approves_green_path() -> None:
    response = client.get("/api/scenarios/tier-one-landmark-route/run")

    assert response.status_code == 200
    body = response.json()
    assert body["property_risk"] == "low"
    assert body["bank_action"] == "approve"
    assert body["closing_passport_status"] == "generated"
    assert "permit_verified" in body["supply_risk_signals"]
    assert body["project"]["name"] == "Landmark Sukhumvit Tower"


def test_supplier_contrast_endpoint_returns_side_by_side_tracks() -> None:
    response = client.get("/api/demo/supplier-contrast")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "supplier_contrast_demo"
    assert body["off_platform"]["track"] == "without_network"
    assert "Shadow Bay" in body["off_platform"]["developer"]
    assert body["off_platform"]["scenario_id"] == "prelaunch-off-platform-route"
    assert body["off_platform"]["closing_passport_status"] == "not_generated"
    assert body["on_network"]["track"] == "with_network"
    assert "Bangkok Landmark" in body["on_network"]["developer"]
    assert body["on_network"]["scenario_id"] == "tier-one-landmark-route"
    assert body["on_network"]["closing_passport_status"] == "generated"
    assert body["on_network"]["feed_snapshot"]["permit_status"] == "issued"


def test_scenario_list_includes_supply_demo_scenarios() -> None:
    response = client.get("/api/scenarios")

    assert response.status_code == 200
    scenario_ids = [item["id"] for item in response.json()["scenarios"]]
    assert "prelaunch-off-platform-route" in scenario_ids
    assert "tier-one-landmark-route" in scenario_ids
    assert len(scenario_ids) == 8
