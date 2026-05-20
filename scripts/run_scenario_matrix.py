#!/usr/bin/env python3
"""Generate docs/SCENARIO_SIMULATION_REPORT.md from all synthetic scenario runs."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STORIES: dict[str, str] = {
    "swift-clean-route": "Clean SWIFT capital, low property and agent risk — FET-ready escrow approved.",
    "usdt-mixed-route": "Amber USDT/wallet mix — conditional approval after conversion evidence.",
    "cash-red-route": "Red cash/P2P capital — reject or legal escalation, no Closing Passport.",
    "mixed-capital-route": "Mixed green/amber/red capital — partial approval and escalation.",
    "developer-suspicious-route": "Green capital but payee authority mismatch — escalate until corrected.",
    "agent-risk-route": "Green capital, high agent pressure — conditional escrow with agent review.",
    "prelaunch-off-platform-route": "Prelaunch sales without permit, off-platform — block bankable route.",
    "tier-one-landmark-route": "Tier-1 on-network developer — green path, Closing Passport generated.",
}

GROUPS: list[tuple[str, list[str]]] = [
    (
        "Capital layer",
        ["swift-clean-route", "usdt-mixed-route", "cash-red-route", "mixed-capital-route"],
    ),
    (
        "Counterparty risk",
        ["developer-suspicious-route", "agent-risk-route"],
    ),
    (
        "Developer supply",
        ["prelaunch-off-platform-route", "tier-one-landmark-route"],
    ),
]


def _load_scenario_ids() -> list[str]:
    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    from app.services.data_loader import load_json  # noqa: E402

    return [item["id"] for item in load_json("scenarios/scenarios.json")["scenarios"]]


def _run_scenarios_local(scenario_ids: list[str]) -> dict[str, dict | None]:
    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    from app.services.scenarios import run_scenario  # noqa: E402

    return {sid: run_scenario(sid) for sid in scenario_ids}


def _run_scenarios_api(api_url: str, scenario_ids: list[str]) -> dict[str, dict | None]:
    import json
    import urllib.error
    import urllib.request

    base = api_url.rstrip("/")
    runs: dict[str, dict | None] = {}
    for sid in scenario_ids:
        with urllib.request.urlopen(f"{base}/api/scenarios/{sid}/run", timeout=30) as response:
            runs[sid] = json.loads(response.read().decode("utf-8"))
    return runs


def _judge_line(bank_action: str) -> str:
    mapping = {
        "approve": "Green path — bank may proceed to bankable escrow.",
        "conditional_approve": "Conditional — additional evidence required before release.",
        "reject": "Reject — do not move funds on this route.",
        "escalate": "Escalate — human compliance review before any release.",
    }
    return mapping.get(bank_action, bank_action)


def _format_scenario_block(scenario_id: str, run: dict) -> str:
    signals = run.get("supply_risk_signals") or []
    signals_line = ", ".join(signals) if signals else "none"
    return f"""### `{scenario_id}`

**Story:** {STORIES.get(scenario_id, scenario_id)}

| Field | Value |
|-------|--------|
| Project | {run["project"]["name"]} |
| Capital | {run["capital_status"]} |
| Property risk | {run["property_risk"]} |
| Agent risk | {run["agent_risk"]} |
| Route decision | `{run["route_decision"]}` |
| Bank action | **{run["bank_action"]}** |
| Closing Passport | {run["closing_passport_status"]} |
| Supply signals | {signals_line} |

**Judge line:** {_judge_line(run["bank_action"])}
"""


def build_report(runs: dict[str, dict | None], scenario_ids: list[str], source_note: str) -> str:
    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Scenario Simulation Report",
        "",
        f"> Generated: {generated} · synthetic demo data · API v0.5.13",
        "",
        f"Batch run of all scenario branches for hackathon judges. Source: {source_note}.",
        "",
        "## Summary matrix",
        "",
        "| Scenario | Capital | Property | Agent | Bank action | Passport |",
        "|----------|---------|----------|-------|-------------|----------|",
    ]

    for sid in scenario_ids:
        run = runs[sid]
        if run is None:
            continue
        lines.append(
            f"| `{sid}` | {run['capital_status']} | {run['property_risk']} | "
            f"{run['agent_risk']} | {run['bank_action']} | {run['closing_passport_status']} |"
        )

    for group_name, ids in GROUPS:
        lines.extend(["", f"## {group_name}", ""])
        for sid in ids:
            run = runs.get(sid)
            if run:
                lines.append(_format_scenario_block(sid, run))

    lines.extend(
        [
            "",
            "## Related",
            "",
            "- [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md)",
            "- [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SCENARIO_SIMULATION_REPORT.md")
    parser.add_argument(
        "--api-url",
        default="",
        help="If set, call GET /api/scenarios/{id}/run on this base URL (e.g. http://localhost:8080)",
    )
    args = parser.parse_args()

    scenario_ids = _load_scenario_ids()
    if args.api_url.strip():
        runs = _run_scenarios_api(args.api_url.strip(), scenario_ids)
        source_note = f"`scripts/run_scenario_matrix.py --api-url {args.api_url.strip()}`"
    else:
        runs = _run_scenarios_local(scenario_ids)
        source_note = "`scripts/run_scenario_matrix.py` (in-process)"

    output = ROOT / "docs" / "SCENARIO_SIMULATION_REPORT.md"
    output.write_text(build_report(runs, scenario_ids, source_note), encoding="utf-8")
    print(f"Wrote {output} ({len(scenario_ids)} scenarios)")


if __name__ == "__main__":
    main()
