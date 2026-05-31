"""Tests for wallet taint providers."""

import os

from app.services.wallet_taint import (
    CAPITAL_CLASS_GREEN,
    ChainalysisStubProvider,
    MockTaintProvider,
    classify_wallet,
    get_taint_provider,
)


def test_classify_wallet_empty() -> None:
    report = classify_wallet("")
    assert report.capital_class == CAPITAL_CLASS_GREEN


def test_classify_wallet_unknown_green() -> None:
    report = classify_wallet("0x0000000000000000000000000000000000000abc")
    assert report.capital_class == CAPITAL_CLASS_GREEN
    assert report.provider == "mock"


def test_classify_wallet_red_mixer() -> None:
    report = classify_wallet("0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f")
    assert report.capital_class == 2
    assert "tornado_cash_2_hop" in report.signals


def test_classify_wallet_case_insensitive() -> None:
    report = classify_wallet("0x23618E81E3F5CDF7F54C3D65F7FBC0ABF5B21E8F")
    assert report.capital_class == 2


def test_chainalysis_stub_without_api_key() -> None:
    provider = ChainalysisStubProvider()
    report = provider.classify("0xabc")
    assert report.error is not None
    assert report.provider == "chainalysis_stub"
    assert "chainalysis_not_configured" in report.signals


def test_get_taint_provider_chainalysis_stub(monkeypatch) -> None:
    monkeypatch.setenv("ATTESTRWA_TAINT_PROVIDER", "chainalysis_stub")
    provider = get_taint_provider()
    assert provider.name == "chainalysis_stub"
    report = provider.classify("0x1")
    assert report.error is not None
