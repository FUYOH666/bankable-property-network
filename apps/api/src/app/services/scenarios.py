import hashlib
from typing import Any

from app.services.data_loader import load_json

SENSITIVE_FIELDS = ["passport_number", "email", "phone", "address", "full_name"]


def _by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def load_scenario_context() -> dict[str, Any]:
    return {
        "scenarios": load_json("scenarios/scenarios.json")["scenarios"],
        "projects": _by_id(load_json("projects/projects.json")["projects"]),
        "agents": _by_id(load_json("agents/agents.json")["agents"]),
        "buyers": _by_id(load_json("buyers/buyers.json")["buyers"]),
        "banks": _by_id(load_json("banks/banks.json")["banks"]),
    }


def list_scenarios() -> list[dict[str, Any]]:
    return load_scenario_context()["scenarios"]


def get_scenario_detail(scenario_id: str) -> dict[str, Any] | None:
    context = load_scenario_context()
    scenario = next((item for item in context["scenarios"] if item["id"] == scenario_id), None)
    if scenario is None:
        return None

    return {
        **scenario,
        "buyer": context["buyers"][scenario["buyer_id"]],
        "project": context["projects"][scenario["project_id"]],
        "agent": context["agents"][scenario["agent_id"]],
        "banks": [context["banks"][bank_id] for bank_id in scenario["bank_path"]],
    }


def _bank_action_for(scenario: dict[str, Any]) -> str:
    if scenario["capital_status"] == "red":
        return "reject"
    if scenario["property_status"] == "high" or scenario["agent_status"] == "high":
        return "escalate"
    if scenario["capital_status"] in {"amber", "mixed"} or scenario["property_status"] == "amber":
        return "conditional_approve"
    return "approve"


def _supply_risk_signals(project: dict[str, Any]) -> list[str]:
    project_id = project.get("id", "")
    if project_id == "project-shadow-red":
        return [
            "prelaunch_without_permit",
            "eia_not_cleared",
            "unverified_sales_entity",
            "off_platform_no_hub",
        ]
    if project_id == "project-landmark-tower":
        return [
            "permit_verified",
            "eia_cleared",
            "licensed_sales_entity",
            "tier_one_on_network",
        ]
    signals: list[str] = []
    if project.get("permit_status") == "pending":
        signals.append("prelaunch_without_permit")
    if project.get("payment_account_status") == "unmatched":
        signals.append("payee_unmatched")
    return signals


def _rag_trace_for(detail: dict[str, Any]) -> list[dict[str, str]]:
    trace = [
        {
            "kind": "policy",
            "document_id": "property_settlement_policy",
            "reason": "Defines capital classification, payee authority, and escrow release requirements.",
        },
        {
            "kind": "developer_profile",
            "document_id": detail["project"]["developer_id"],
            "reason": f"Project status is {detail['project']['status']} with {detail['project']['payment_account_status']} payment account status.",
        },
        {
            "kind": "agent_profile",
            "document_id": detail["agent"]["id"],
            "reason": f"Agent status is {detail['agent']['status']} with {detail['agent']['commission_disclosure']} commission disclosure.",
        },
        {
            "kind": "payment_instruction",
            "document_id": "doc-payment-instruction",
            "reason": "Used to compare expected developer/payee with instructed receiving entity.",
        },
        {
            "kind": "route_rule",
            "document_id": "settlement_rules/routes",
            "reason": f"Route decision is {detail['route_decision']}.",
        },
        {
            "kind": "compliance_memo",
            "document_id": "doc-compliance-memo",
            "reason": "Human-readable rationale for approval, rejection, or escalation.",
        },
    ]
    project_id = detail["project"].get("id", "")
    if project_id == "project-shadow-red":
        trace.append(
            {
                "kind": "supply_risk",
                "document_id": "documents/prelaunch_permit_risk_brief.md",
                "reason": "Prelaunch sales without construction permit — off-platform buyer risk.",
            }
        )
        trace.append(
            {
                "kind": "policy",
                "document_id": "policies/prelaunch_sales_policy.md",
                "reason": "Bank policy blocks settlement until permit and licensed sales entity verified.",
            }
        )
    if project_id == "project-landmark-tower":
        trace.append(
            {
                "kind": "supply_risk",
                "document_id": "documents/tier_one_developer_verification_pack.md",
                "reason": "Tier-1 developer verification pack — permit, EIA, payee matched.",
            }
        )
    return trace


def run_scenario(scenario_id: str) -> dict[str, Any] | None:
    detail = get_scenario_detail(scenario_id)
    if detail is None:
        return None

    bank_action = _bank_action_for(detail)
    closing_passport_status = detail["closing_passport"]
    evidence_hash = None
    if closing_passport_status != "not_generated":
        evidence_hash = "0x" + hashlib.sha256(detail["id"].encode("utf-8")).hexdigest()

    return {
        "id": detail["id"],
        "capital_status": detail["capital_status"],
        "property_risk": detail["property_status"],
        "agent_risk": detail["agent_status"],
        "route_decision": detail["route_decision"],
        "bank_action": bank_action,
        "closing_passport_status": closing_passport_status,
        "closing_passport_hash": evidence_hash,
        "supply_risk_signals": _supply_risk_signals(detail["project"]),
        "buyer": detail["buyer"],
        "project": detail["project"],
        "agent": detail["agent"],
        "banks": detail["banks"],
        "evidence_preview": {
            "included": ["scenario_id", "buyer_id", "project_id", "agent_id", "bank_path", "route_decision", "bank_action"],
            "excluded_sensitive_fields": SENSITIVE_FIELDS,
            "privacy_note": "Scenario evidence contains synthetic IDs, statuses, and extracted facts only.",
        },
        "rag_trace": _rag_trace_for(detail),
    }
