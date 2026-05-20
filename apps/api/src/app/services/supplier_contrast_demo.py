from typing import Any

from app.services.data_loader import load_json
from app.services.developer_knowledge import (
    LANDMARK_FEED,
    SHADOW_FEED,
    build_feed_summary,
)
from app.services.scenarios import run_scenario

OFF_PLATFORM_SCENARIO = "prelaunch-off-platform-route"
ON_NETWORK_SCENARIO = "tier-one-landmark-route"


def build_supplier_contrast_demo() -> dict[str, Any]:
    off_run = run_scenario(OFF_PLATFORM_SCENARIO)
    on_run = run_scenario(ON_NETWORK_SCENARIO)
    if off_run is None or on_run is None:
        raise ValueError("Supplier contrast scenarios are not configured")

    shadow_feed = load_json(SHADOW_FEED)
    landmark_feed = load_json(LANDMARK_FEED)

    return {
        "data_classification": "synthetic_demo_data",
        "module": "supplier_contrast_demo",
        "pitch_line": (
            "Developers join the network before buyers arrive. "
            "Off-platform prelaunch sales hide permit and payee risk — on-network tier-1 feeds enable bankable escrow."
        ),
        "off_platform": {
            "track": "without_network",
            "developer": shadow_feed["developer_name"],
            "project": shadow_feed["project_name"],
            "scenario_id": OFF_PLATFORM_SCENARIO,
            "headline": "Buyer off-network hits prelaunch sales before permits",
            "risk_summary": (
                "Units marketed without construction permit. Agent pressure. "
                "Payee not in authorized feed. No Closing Passport."
            ),
            "permit_status": shadow_feed.get("permit_status", "unknown"),
            "eia_status": shadow_feed.get("eia_status", "unknown"),
            "sales_status": shadow_feed.get("sales_status", "unknown"),
            "network_status": shadow_feed.get("network_status", "off_platform"),
            "marketing_payee_claimed": shadow_feed.get("marketing_payee_claimed"),
            "bank_action": off_run["bank_action"],
            "closing_passport_status": off_run["closing_passport_status"],
            "supply_risk_signals": off_run.get("supply_risk_signals", []),
            "scenario_run": {
                "property_risk": off_run["property_risk"],
                "route_decision": off_run["route_decision"],
            },
        },
        "on_network": {
            "track": "with_network",
            "developer": landmark_feed["developer_name"],
            "project": landmark_feed["project_name"],
            "scenario_id": ON_NETWORK_SCENARIO,
            "headline": "Tier-1 developer on-network — verified feed, green path",
            "risk_summary": (
                "Permit issued, EIA cleared, licensed sales entity matched. "
                "Inventory and payee from ERP feed. FET-ready escrow and Closing Passport."
            ),
            "feed_snapshot": build_feed_summary(LANDMARK_FEED)["feed_snapshot"],
            "reputation_tier": landmark_feed.get("reputation_tier", "tier_one"),
            "bank_action": on_run["bank_action"],
            "closing_passport_status": on_run["closing_passport_status"],
            "supply_risk_signals": on_run.get("supply_risk_signals", []),
            "scenario_run": {
                "property_risk": on_run["property_risk"],
                "route_decision": on_run["route_decision"],
            },
        },
    }
