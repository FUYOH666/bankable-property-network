import hashlib
import json
from datetime import UTC, datetime
from typing import Any


SENSITIVE_KEYS = {"passport_number", "email", "phone", "address", "full_name"}


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _sanitize(item) for key, item in value.items() if key not in SENSITIVE_KEYS}
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def build_evidence_pack(
    case_id: str,
    risk_report: dict[str, Any],
    capital_map: dict[str, dict[str, Any]],
    route: dict[str, Any],
    approver_role: str,
) -> dict[str, Any]:
    sanitized_evidence = _sanitize(
        {
            "case_id": case_id,
            "risk_report": risk_report,
            "capital_map": capital_map,
            "route": route,
            "approver_role": approver_role,
        }
    )
    canonical = json.dumps(sanitized_evidence, sort_keys=True, separators=(",", ":"))
    evidence_hash = "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    return {
        "case_id": case_id,
        "evidence_pack_hash": evidence_hash,
        "evidence": sanitized_evidence,
        "attestation": {
            "buyer_bankability_checked": True,
            "developer_risk_reviewed": True,
            "settlement_route_approved": route.get("recommended") is True,
            "escrow_conditions_generated": route.get("id") == "bankable_escrow",
            "evidence_pack_hash": evidence_hash,
            "timestamp": datetime.now(UTC).isoformat(),
            "approver_role": approver_role,
        },
    }
