from app.services.capital import classify_capital_sources
from app.services.evidence_pack import build_evidence_pack
from app.services.risk_engine import analyze_property_risk
from app.services.routing import compare_settlement_routes, pick_recommended_route


def test_property_shield_flags_wrong_legal_entity_deposit_request() -> None:
    case = {
        "developer_name": "Siam Riverside Living",
        "expected_payee": "Siam Riverside Living Co., Ltd.",
        "payment_instruction_payee": "SRL Holding 2026 Co., Ltd.",
        "deposit_deadline_hours": 12,
        "documents": ["booking_request"],
    }

    report = analyze_property_risk(case)

    assert report["risk_level"] == "high"
    assert "payment_instruction_mismatch" in report["flags"]
    assert "suspicious_urgency" in report["flags"]
    assert "missing_buyer_protection_clause" in report["flags"]


def test_capital_bankability_map_classifies_bank_usdt_and_p2p_sources() -> None:
    sources = [
        {"id": "src-bank-sg", "kind": "bank_transfer", "amount": 50000, "currency": "USD", "proof": "bank_statement"},
        {"id": "src-usdt", "kind": "stablecoin", "amount": 180000, "currency": "USDT", "wallet_summary": "explainable"},
        {"id": "src-p2p", "kind": "p2p_cash", "amount": 900000, "currency": "THB"},
    ]

    result = classify_capital_sources(sources)

    assert result["src-bank-sg"]["status"] == "green"
    assert result["src-usdt"]["status"] == "amber"
    assert result["src-p2p"]["status"] == "red"


def test_route_comparison_prefers_bankable_escrow_when_risk_is_high() -> None:
    routes = compare_settlement_routes(
        risk_level="high",
        capital_map={
            "src-bank-sg": {"status": "green"},
            "src-usdt": {"status": "amber"},
            "src-p2p": {"status": "red"},
        },
    )

    recommended = pick_recommended_route(routes)

    assert recommended["id"] == "bankable_escrow"
    assert "verified payee" in " ".join(recommended["conditions"]).lower()


def test_evidence_pack_hash_is_deterministic_and_excludes_sensitive_fields() -> None:
    pack = build_evidence_pack(
        case_id="case-anchor-deposit-mismatch",
        risk_report={"risk_level": "high", "flags": ["payment_instruction_mismatch"]},
        capital_map={"src-bank-sg": {"status": "green", "passport_number": "SHOULD-NOT-LEAK"}},
        route={"id": "bankable_escrow", "recommended": True},
        approver_role="bank_compliance",
    )
    pack_again = build_evidence_pack(
        case_id="case-anchor-deposit-mismatch",
        risk_report={"risk_level": "high", "flags": ["payment_instruction_mismatch"]},
        capital_map={"src-bank-sg": {"status": "green", "passport_number": "SHOULD-NOT-LEAK"}},
        route={"id": "bankable_escrow", "recommended": True},
        approver_role="bank_compliance",
    )

    assert pack["evidence_pack_hash"] == pack_again["evidence_pack_hash"]
    assert pack["attestation"]["buyer_bankability_checked"] is True
    assert "passport_number" not in str(pack)
