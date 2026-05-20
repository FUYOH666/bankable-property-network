"""Tests for the attester decision logic (pure, no on-chain submission)."""

from __future__ import annotations

from app.services.attester_service import DealRequest, decide_for_deal


# Wallet addresses from data/synthetic/rwa/wallets.json
BUYER_CLEAN = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
BUYER_TAINTED = "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"
PAYEE_LANDMARK_OK = "0x976EA74026E726554dB657fA54763abd0C3a0aa9"
PAYEE_SRL_HOLDING_IMPOSTOR = "0x90F79bf6EB2c4f870365E785982E1f101E93b906"
PAYEE_SIAM_OK = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
MOCK_USDC = "0xeba5CEc9257045Df0B44eA784F9a7Fa07DeeF6d4"


def _request(**overrides):
    base = {
        "deal_id": b"\x01" * 32,
        "buyer_wallet": BUYER_CLEAN,
        "payee_wallet": PAYEE_LANDMARK_OK,
        "token_address": MOCK_USDC,
        "amount_base_units": 580_000_000,
        "developer_id": "developer-bangkok-landmark",
        "jurisdiction": "TH",
        "buyer_kyc_tier": 3,
        "expires_in_seconds": 86_400,
    }
    base.update(overrides)
    return DealRequest(**base)


def test_happy_path_approves_bangkok_landmark() -> None:
    decision = decide_for_deal(_request())
    assert decision.decision == "approve"
    assert decision.payee_verified is True
    assert decision.capital_class == 0
    assert decision.reasons == []
    assert all(r["passed"] for r in decision.rule_results)
    assert len(decision.evidence_hash) == 32
    assert decision.expires_at > 0


def test_payee_mismatch_rejects() -> None:
    decision = decide_for_deal(
        _request(
            developer_id="siam-riverside-living",
            payee_wallet=PAYEE_SRL_HOLDING_IMPOSTOR,
        )
    )
    assert decision.decision == "reject"
    assert decision.payee_verified is False
    assert any("authorized_payee_wallets" in r for r in decision.reasons)


def test_capital_red_rejects() -> None:
    decision = decide_for_deal(
        _request(
            buyer_wallet=BUYER_TAINTED,
            payee_wallet=PAYEE_LANDMARK_OK,
            developer_id="developer-bangkok-landmark",
        )
    )
    assert decision.decision == "reject"
    assert decision.capital_class == 2
    assert any("capital_class" in r for r in decision.reasons)


def test_siam_riverside_happy_path() -> None:
    decision = decide_for_deal(
        _request(
            developer_id="siam-riverside-living",
            payee_wallet=PAYEE_SIAM_OK,
        )
    )
    assert decision.decision == "approve"
    assert decision.payee_verified is True


def test_shadow_bay_has_no_authorized_payees() -> None:
    decision = decide_for_deal(
        _request(
            developer_id="developer-shadow-bay",
            payee_wallet=PAYEE_LANDMARK_OK,
        )
    )
    assert decision.decision == "reject"
    assert decision.payee_verified is False


def test_unsupported_jurisdiction_rejects() -> None:
    decision = decide_for_deal(_request(jurisdiction="US"))
    assert decision.decision == "reject"
    assert any("only-supported-jurisdictions" in r for r in decision.reasons)
