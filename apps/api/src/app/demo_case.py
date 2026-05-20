from typing import Any


INFRASTRUCTURE_CONTEXT: dict[str, str] = {
    "failure_mode": "unverified_settlement_path",
    "root_cause": "developer_paid_commissions_no_entry_barrier",
    "narrative_role": "demo_illustration_not_buyer_blame",
    "primary_customer": "banking_anchor",
}


ANCHOR_CASE: dict[str, Any] = {
    "id": "case-anchor-deposit-mismatch",
    "title": "Infrastructure failure: unverified settlement path on 12M THB condo deposit",
    "network_positioning": "bankable_property_network",
    "buyer_profile": "Foreign buyer purchasing a 12M THB Bangkok condo with Dubai bank funds and USDT holdings.",
    "settlement_context": "Dubai bank originator to Thai bank FET-ready settlement route with escrow conditions.",
    "developer_name": "Siam Riverside Living Co., Ltd.",
    "expected_payee": "Siam Riverside Living Co., Ltd.",
    "payment_instruction_payee": "SRL Holding 2026 Co., Ltd.",
    "deposit_deadline_hours": 12,
    "documents": ["booking_request", "developer_profile", "payment_instruction_letter"],
    "risk_signals": ["legal_entity_changed"],
    "capital_sources": [
        {"id": "src-bank-dubai", "kind": "bank_transfer", "amount": 50000, "currency": "USD", "proof": "bank_statement"},
        {"id": "src-usdt", "kind": "stablecoin", "amount": 180000, "currency": "USDT", "wallet_summary": "explainable"},
        {"id": "src-p2p", "kind": "p2p_cash", "amount": 900000, "currency": "THB"},
    ],
}
