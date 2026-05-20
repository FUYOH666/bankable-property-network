from typing import Any

from app.services.data_loader import load_json

DEFAULT_MANAGER_ID = "mgr-riverside-partner"
MONTHLY_RENT_CONSERVATIVE = 38_000
MONTHLY_RENT_OPTIMISTIC = 48_000
MANAGEMENT_FEE_PCT = 10
VACANCY_RESERVE_PCT = 5


def _find_manager(managers: list[dict[str, Any]], manager_id: str) -> dict[str, Any]:
    for manager in managers:
        if manager["id"] == manager_id:
            return manager
    if managers:
        return managers[0]
    return {
        "id": "unknown",
        "name": "Unknown manager",
        "verified_by_platform": False,
        "units_managed": 0,
        "average_occupancy_pct": 0,
        "complaint_rate": "unknown",
        "management_fee_pct": 0,
        "specialization": "No verified manager on file",
    }


def _purchase_price_thb(case: dict[str, Any]) -> int:
    if case.get("purchase_price_thb"):
        return int(case["purchase_price_thb"])
    feed = load_json("developers/siam-riverside-feed.json")
    units = feed.get("units_available", [])
    if units:
        return int(units[0].get("price_thb", 12_000_000))
    return 12_000_000


def _net_yield_range(purchase_price_thb: int, monthly_rent_low: int, monthly_rent_high: int) -> dict[str, Any]:
    def annual_net(monthly_rent: int) -> float:
        gross = monthly_rent * 12
        net = gross * (1 - (MANAGEMENT_FEE_PCT + VACANCY_RESERVE_PCT) / 100)
        return round((net / purchase_price_thb) * 100, 1)

    return {
        "conservative_pct": annual_net(monthly_rent_low),
        "base_pct": annual_net((monthly_rent_low + monthly_rent_high) // 2),
        "optimistic_pct": annual_net(monthly_rent_high),
        "display_range": f"{annual_net(monthly_rent_low)}–{annual_net(monthly_rent_high)}%",
    }


def build_post_closing_yield_plan(case: dict[str, Any]) -> dict[str, Any]:
    managers_data = load_json("rental/managers.json")
    restrictions_data = load_json("rental/building_restrictions.json")

    building = restrictions_data["buildings"][0]
    rental_modes = building["rental_modes"]
    recommended_manager = _find_manager(managers_data["managers"], DEFAULT_MANAGER_ID)
    purchase_price_thb = _purchase_price_thb(case)
    yield_estimate = _net_yield_range(purchase_price_thb, MONTHLY_RENT_CONSERVATIVE, MONTHLY_RENT_OPTIMISTIC)

    return {
        "data_classification": "synthetic_demo_data",
        "module": "post_closing_yield_plan",
        "vision_note": "Strategic extension teaser. Not a production rental platform.",
        "case_id": case["id"],
        "property_summary": {
            "purchase_price_thb": purchase_price_thb,
            "developer": case["developer_name"],
            "building": building["building_name"],
        },
        "after_purchase": {
            "recommended_rental_model": "12-month expat lease",
            "short_term_rental": "not recommended until building/license verification",
            "verified_manager_available": recommended_manager.get("verified_by_platform", False),
            "estimated_net_yield": yield_estimate["display_range"],
            "yield_breakdown": yield_estimate,
            "rental_income_account": "Open with partner bank after Closing Passport",
            "next_action": "Assign verified property manager",
        },
        "legal_rental_mode": {
            "long_term_lease": rental_modes["long_term_lease_12m"],
            "expat_rental_3_12m": rental_modes["expat_rental_3_12m"],
            "short_term_under_30_days": rental_modes["short_term_under_30_days"],
            "serviced_apartment_hotel_model": rental_modes["serviced_apartment_hotel_model"],
            "juristic_person_restriction": building["juristic_person_restriction"],
        },
        "verified_managers": managers_data["managers"],
        "recommended_manager": recommended_manager,
        "bank_value": {
            "rental_income_account": "Monthly rent collection on bank rails",
            "ongoing_relationship": "Management fees, maintenance reserves, insurance, tax reporting",
            "pitch_line": "Most platforms stop when the property is sold. Banks should not.",
        },
    }
