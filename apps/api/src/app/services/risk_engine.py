from typing import Any


def analyze_property_risk(case: dict[str, Any]) -> dict[str, Any]:
    flags: list[str] = []

    expected_payee = case.get("expected_payee")
    payment_payee = case.get("payment_instruction_payee")
    if expected_payee and payment_payee and expected_payee != payment_payee:
        flags.append("payment_instruction_mismatch")

    if int(case.get("deposit_deadline_hours", 999)) <= 24:
        flags.append("suspicious_urgency")

    documents = set(case.get("documents", []))
    if "buyer_protection_clause" not in documents:
        flags.append("missing_buyer_protection_clause")

    if "legal_entity_changed" in case.get("risk_signals", []):
        flags.append("legal_entity_change")

    risk_level = "high" if {"payment_instruction_mismatch", "suspicious_urgency"} <= set(flags) else "medium"
    if not flags:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "flags": flags,
        "summary": "Deposit should not move until payee authority and escrow conditions are verified.",
        "recommended_next_action": "Escalate to bank compliance and request corrected payment instructions.",
    }
