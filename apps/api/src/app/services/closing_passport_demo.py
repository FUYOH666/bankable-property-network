from functools import lru_cache
from typing import Any

from app.demo_case import ANCHOR_CASE, INFRASTRUCTURE_CONTEXT
from app.services.capital import classify_capital_sources
from app.services.evidence_pack import build_evidence_pack
from app.services.risk_engine import analyze_property_risk
from app.services.routing import compare_settlement_routes, pick_recommended_route


@lru_cache(maxsize=1)
def build_closing_passport_demo() -> dict[str, Any]:
    risk_report = analyze_property_risk(ANCHOR_CASE)
    capital_map = classify_capital_sources(ANCHOR_CASE["capital_sources"])
    routes = compare_settlement_routes(risk_report["risk_level"], capital_map)
    recommended_route = pick_recommended_route(routes)
    closing_passport = build_evidence_pack(
        case_id=ANCHOR_CASE["id"],
        risk_report=risk_report,
        capital_map=capital_map,
        route=recommended_route,
        approver_role="bank_compliance",
    )

    return {
        "case": ANCHOR_CASE,
        "property_shield": risk_report,
        "capital_bankability_map": capital_map,
        "routes": routes,
        "recommended_route": recommended_route,
        "bank_counter_offer": {
            "product": "Verified escrow + FET-ready settlement package",
            "offer": "Hold deposit until payee authority is verified, then release through bankable escrow.",
            "buyer_value": "Avoid sending an irreversible deposit to the wrong legal entity.",
            "bank_value": "Capture high-value settlement flow before it leaves bankable rails.",
        },
        "closing_passport": closing_passport,
        "infrastructure_context": INFRASTRUCTURE_CONTEXT,
    }
