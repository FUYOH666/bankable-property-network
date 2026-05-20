from typing import Any


def compare_settlement_routes(risk_level: str, capital_map: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    has_red_source = any(source["status"] == "red" for source in capital_map.values())
    prefer_escrow = risk_level == "high" or has_red_source

    return [
        {
            "id": "direct_agent_deposit",
            "label": "Direct agent deposit",
            "recommended": False,
            "risk": "high",
            "conditions": ["Do not send irreversible deposit while payee authority is unresolved."],
        },
        {
            "id": "crypto_p2p_route",
            "label": "Crypto/P2P conversion route",
            "recommended": False,
            "risk": "high" if has_red_source else "medium",
            "conditions": ["Requires verified counterparty, wallet history, and source-of-funds memo."],
        },
        {
            "id": "bankable_escrow",
            "label": "Bankable escrow route",
            "recommended": True,
            "risk": "controlled",
            "conditions": [
                "Verified payee legal authority before deposit release.",
                "Escrow release only after corrected payment instructions and compliance approval.",
                "Evidence pack retained for buyer, bank, and audit review.",
            ]
            + ([] if prefer_escrow else ["Preferred bank-grade route even when capital profile is clean."]),
        },
    ]


def pick_recommended_route(routes: list[dict[str, Any]]) -> dict[str, Any]:
    recommended = [route for route in routes if route.get("recommended")]
    if len(recommended) == 1:
        return recommended[0]
    if len(recommended) > 1:
        return recommended[0]
    for route in routes:
        if route.get("id") == "bankable_escrow":
            return route
    raise ValueError("No settlement route available")
