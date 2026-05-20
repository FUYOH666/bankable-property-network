"""Tiny YAML rule DSL for AttestRWA compliance policies.

A policy file is a YAML document of the shape:

    rules:
      - id: payee-must-match-developer-feed
        require: payee_verified == true
      - id: capital-not-red
        require: capital_class < 2
      - id: kyc-tier-by-amount
        require: amount <= 100000 or buyer_kyc_tier >= 3

The expression after `require:` is a single Python boolean expression
evaluated against a fixed, validated context. The evaluator is deliberately
narrow — only AND/OR/NOT, comparisons (==, !=, <, <=, >, >=), and bare
identifiers / numeric / boolean / string literals are allowed. No
attribute access, no function calls, no subscription, no walrus.

This lets banks publish policy packs as plain text and the escrow flow stays
deterministic without embedding a full interpreter.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_ALLOWED_NODES: tuple[type, ...] = (
    ast.Expression,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.UnaryOp,
    ast.Not,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Constant,
    ast.Name,
    ast.Load,
)


class DSLError(ValueError):
    """Raised when a rule file or expression is malformed."""


@dataclass(slots=True, frozen=True)
class Rule:
    """A single declarative rule."""

    id: str
    expression: str


@dataclass(slots=True, frozen=True)
class RuleResult:
    """Outcome of evaluating one rule against a context."""

    rule_id: str
    passed: bool
    explanation: str


@dataclass(slots=True, frozen=True)
class PolicyEvaluation:
    """Outcome of evaluating a full policy."""

    decision: str  # "approve" | "reject"
    rule_results: list[RuleResult]

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.rule_results)


def _validate_ast(node: ast.AST) -> None:
    for sub in ast.walk(node):
        if not isinstance(sub, _ALLOWED_NODES):
            raise DSLError(
                f"DSL expression contains disallowed node {type(sub).__name__}"
            )
        if isinstance(sub, ast.Name) and sub.id in {"__import__", "eval", "exec", "open"}:
            raise DSLError(f"DSL expression references forbidden name {sub.id!r}")


def parse_rules(source: str | Path) -> list[Rule]:
    """Parse a YAML rule file or string into a list of `Rule`."""
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
    else:
        text = source
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise DSLError(f"YAML parse error: {exc}") from exc

    if not isinstance(doc, dict) or "rules" not in doc:
        raise DSLError("DSL document must be a mapping with a 'rules' key")
    if not isinstance(doc["rules"], list):
        raise DSLError("'rules' must be a list")

    rules: list[Rule] = []
    for entry in doc["rules"]:
        if not isinstance(entry, dict):
            raise DSLError(f"each rule must be a mapping; got {entry!r}")
        rule_id = entry.get("id")
        expression = entry.get("require")
        if not isinstance(rule_id, str) or not isinstance(expression, str):
            raise DSLError(f"each rule needs string 'id' and 'require'; got {entry!r}")
        ast_tree = ast.parse(expression, mode="eval")
        _validate_ast(ast_tree)
        rules.append(Rule(id=rule_id, expression=expression))
    return rules


def evaluate(rules: list[Rule], context: dict[str, Any]) -> PolicyEvaluation:
    """Evaluate a list of rules against a context dict; first failure stops."""
    safe_globals: dict[str, Any] = {"__builtins__": {}}
    safe_locals: dict[str, Any] = {
        # YAML-style boolean aliases so rule authors can write
        # `payee_verified == true` instead of Python's `True`.
        "true": True,
        "false": False,
        "null": None,
    }
    safe_locals.update(context)
    results: list[RuleResult] = []
    for rule in rules:
        try:
            outcome = eval(  # noqa: S307 — AST has been validated
                compile(rule.expression, f"<rule:{rule.id}>", mode="eval"),
                safe_globals,
                safe_locals,
            )
        except NameError as exc:
            raise DSLError(
                f"Rule {rule.id!r} referenced unknown context name: {exc}"
            ) from exc
        passed = bool(outcome)
        explanation = (
            f"{rule.expression} -> {outcome!r}"
            if passed
            else f"{rule.expression} did not hold (evaluated to {outcome!r})"
        )
        results.append(RuleResult(rule_id=rule.id, passed=passed, explanation=explanation))
        if not passed:
            break
    decision = "approve" if all(r.passed for r in results) else "reject"
    return PolicyEvaluation(decision=decision, rule_results=results)
