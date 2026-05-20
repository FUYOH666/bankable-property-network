import pytest

from app.services.compliance_dsl import DSLError, evaluate, parse_rules


GOOD_POLICY = """
rules:
  - id: payee-must-match
    require: payee_verified == true
  - id: capital-not-red
    require: capital_class < 2
"""


def test_parse_rules_happy_path() -> None:
    rules = parse_rules(GOOD_POLICY)
    assert len(rules) == 2
    assert rules[0].id == "payee-must-match"
    assert rules[1].id == "capital-not-red"


def test_evaluate_approve_when_all_pass() -> None:
    rules = parse_rules(GOOD_POLICY)
    out = evaluate(rules, {"payee_verified": True, "capital_class": 0})
    assert out.decision == "approve"
    assert all(r.passed for r in out.rule_results)


def test_evaluate_reject_on_first_fail() -> None:
    rules = parse_rules(GOOD_POLICY)
    out = evaluate(rules, {"payee_verified": False, "capital_class": 0})
    assert out.decision == "reject"
    assert out.rule_results[0].passed is False
    assert len(out.rule_results) == 1  # short-circuit


def test_evaluate_reject_when_capital_red() -> None:
    rules = parse_rules(GOOD_POLICY)
    out = evaluate(rules, {"payee_verified": True, "capital_class": 2})
    assert out.decision == "reject"
    assert any(not r.passed for r in out.rule_results)


def test_disallows_function_calls() -> None:
    bad = """
rules:
  - id: bad
    require: print("hi")
"""
    with pytest.raises(DSLError):
        parse_rules(bad)


def test_disallows_attribute_access() -> None:
    bad = """
rules:
  - id: bad
    require: payee.attr == true
"""
    with pytest.raises(DSLError):
        parse_rules(bad)


def test_missing_context_name_raises() -> None:
    rules = parse_rules(GOOD_POLICY)
    with pytest.raises(DSLError):
        evaluate(rules, {})
