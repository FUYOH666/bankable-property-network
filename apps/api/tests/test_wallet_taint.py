from app.services.wallet_taint import (
    CAPITAL_CLASS_GREEN,
    CAPITAL_CLASS_RED,
    classify_wallet,
)


def test_empty_wallet_is_green() -> None:
    report = classify_wallet("")
    assert report.capital_class == CAPITAL_CLASS_GREEN
    assert report.signals == []


def test_unknown_wallet_is_green() -> None:
    report = classify_wallet("0x0000000000000000000000000000000000000abc")
    assert report.capital_class == CAPITAL_CLASS_GREEN
    assert report.signals == []
    assert "green" in report.explanation


def test_known_tainted_wallet_is_red() -> None:
    report = classify_wallet("0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f")
    assert report.capital_class == CAPITAL_CLASS_RED
    assert "tornado_cash_2_hop" in report.signals
    assert "sanctioned mixer" in report.explanation.lower()


def test_case_insensitive_match() -> None:
    report = classify_wallet("0x23618E81E3F5CDF7F54C3D65F7FBC0ABF5B21E8F")
    assert report.capital_class == CAPITAL_CLASS_RED
