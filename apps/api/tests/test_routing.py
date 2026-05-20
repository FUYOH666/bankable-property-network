from app.services.routing import compare_settlement_routes, pick_recommended_route


def test_route_comparison_always_has_recommended_route_for_low_risk() -> None:
    routes = compare_settlement_routes(
        risk_level="low",
        capital_map={
            "src-bank-sg": {"status": "green"},
        },
    )

    recommended = pick_recommended_route(routes)

    assert recommended["id"] == "bankable_escrow"
    assert recommended["recommended"] is True


def test_pick_recommended_route_falls_back_to_bankable_escrow() -> None:
    routes = [
        {"id": "direct_agent_deposit", "recommended": False},
        {"id": "bankable_escrow", "recommended": False},
    ]

    recommended = pick_recommended_route(routes)

    assert recommended["id"] == "bankable_escrow"
