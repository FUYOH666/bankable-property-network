"""Policy pack loading tests — ASEAN pack must parse and evaluate."""

from pathlib import Path

import pytest

from app.services.compliance_dsl import evaluate, parse_rules

REPO_ROOT = Path(__file__).resolve().parents[3]
ASEAN_POLICY = REPO_ROOT / "data/policies/asean-property-settlement-v1.yaml"


@pytest.fixture
def asean_rules():
    text = ASEAN_POLICY.read_text(encoding="utf-8")
    return parse_rules(text)


def test_asean_policy_file_exists() -> None:
    assert ASEAN_POLICY.is_file()


def test_asean_policy_parses_four_rules(asean_rules) -> None:
    assert len(asean_rules) == 4
    ids = {r.id for r in asean_rules}
    assert "payee-must-match-developer-feed" in ids
    assert "asean-jurisdictions-only" in ids


def test_asean_approve_happy_path(asean_rules) -> None:
    ctx = {
        "payee_verified": True,
        "capital_class": 0,
        "jurisdiction": "TH",
        "amount_usdc": 580_000_000,
        "buyer_kyc_tier": 3,
    }
    out = evaluate(asean_rules, ctx)
    assert out.decision == "approve"


def test_asean_reject_non_asean_jurisdiction(asean_rules) -> None:
    ctx = {
        "payee_verified": True,
        "capital_class": 0,
        "jurisdiction": "US",
        "amount_usdc": 580_000_000,
        "buyer_kyc_tier": 3,
    }
    out = evaluate(asean_rules, ctx)
    assert out.decision == "reject"


def test_asean_reject_red_capital(asean_rules) -> None:
    ctx = {
        "payee_verified": True,
        "capital_class": 2,
        "jurisdiction": "SG",
        "amount_usdc": 100_000_000,
        "buyer_kyc_tier": 3,
    }
    out = evaluate(asean_rules, ctx)
    assert out.decision == "reject"
