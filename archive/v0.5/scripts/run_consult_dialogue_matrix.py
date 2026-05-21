#!/usr/bin/env python3
"""Generate docs/CONSULT_DIALOGUE_SIMULATION_REPORT.md from multi-turn consult scripts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "data" / "consult_dialogues" / "dialogue_matrix.yaml"


def _load_matrix() -> list[dict[str, Any]]:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        # Minimal YAML loader for our flat dialogue fixtures (no PyYAML in root).
        return _load_matrix_minimal()
    data = yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8"))
    return data["dialogues"]


def _load_matrix_minimal() -> list[dict[str, Any]]:
    """Parse dialogue_matrix.yaml without PyYAML dependency."""
    import ast

    text = MATRIX_PATH.read_text(encoding="utf-8")
    dialogues: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    turn: dict[str, Any] | None = None
    in_expect = False
    expect: dict[str, Any] = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("  - id:"):
            if current:
                if turn:
                    if expect:
                        turn["expect"] = expect
                    current.setdefault("turns", []).append(turn)
                dialogues.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
            turn = None
            expect = {}
            in_expect = False
        elif current is not None and line.startswith("    description:"):
            current["description"] = line.split(":", 1)[1].strip()
        elif current is not None and line.startswith("    channel:"):
            current["channel"] = line.split(":", 1)[1].strip()
        elif line.startswith("      - user:"):
            if turn:
                if expect:
                    turn["expect"] = expect
                current.setdefault("turns", []).append(turn)
            turn = {"user": ast.literal_eval(line.split(":", 1)[1].strip())}
            expect = {}
            in_expect = False
        elif line.strip() == "expect:":
            in_expect = True
        elif in_expect and line.startswith("          "):
            key, _, val = line.strip().partition(":")
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                expect[key] = ast.literal_eval(val)
            elif val.isdigit():
                expect[key] = int(val)
            else:
                expect[key] = val.strip('"')

    if current:
        if turn:
            if expect:
                turn["expect"] = expect
            current.setdefault("turns", []).append(turn)
        dialogues.append(current)
    return dialogues


def _run_offline(dialogues: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
    import os
    from unittest.mock import patch

    from app.services import buyer_consultation as bc
    from app.services.consult_knowledge import load_knowledge_corpus

    load_knowledge_corpus.cache_clear()
    bc._sessions.clear()
    results: dict[str, list[dict[str, Any]]] = {}

    with patch.dict(os.environ, {"CONSULT_RETRIEVAL_MODE": "keyword"}, clear=False):
        with patch.object(bc, "_llm_reply", return_value=None):
            for script in dialogues:
                sid = f"sim-{script['id']}"
                bc._sessions.pop(sid, None)
                turn_results: list[dict[str, Any]] = []
                for turn in script["turns"]:
                    body = bc.handle_consult_message(
                        session_id=sid,
                        message=turn["user"],
                        channel=script.get("channel", "web"),
                    )
                    checks = _evaluate_turn(body, turn.get("expect", {}))
                    turn_results.append(
                        {
                            "user": turn["user"],
                            "response": body,
                            "checks": checks,
                            "passed": all(item["ok"] for item in checks),
                        }
                    )
                results[script["id"]] = turn_results
    return results


def _run_api(api_url: str, dialogues: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    base = api_url.rstrip("/")
    results: dict[str, list[dict[str, Any]]] = {}
    for script in dialogues:
        sid = f"sim-{script['id']}"
        turn_results: list[dict[str, Any]] = []
        for turn in script["turns"]:
            payload = json.dumps(
                {"session_id": sid, "message": turn["user"], "channel": script.get("channel", "web")}
            ).encode("utf-8")
            req = urllib.request.Request(
                f"{base}/api/consult/message",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=180) as response:
                body = json.loads(response.read().decode("utf-8"))
            checks = _evaluate_turn(body, turn.get("expect", {}))
            turn_results.append(
                {
                    "user": turn["user"],
                    "response": body,
                    "checks": checks,
                    "passed": all(item["ok"] for item in checks),
                }
            )
        results[script["id"]] = turn_results
    return results


def _reply_text(body: dict[str, Any]) -> str:
    return (body.get("reply") or "").lower()


def _citations_blob(body: dict[str, Any]) -> str:
    return json.dumps(body.get("citations") or [], ensure_ascii=False).lower()


def _evaluate_turn(body: dict[str, Any], expect: dict[str, Any]) -> list[dict[str, str | bool]]:
    checks: list[dict[str, str | bool]] = []
    reply = _reply_text(body)
    cites = _citations_blob(body)

    if intent := expect.get("intent"):
        ok = body.get("intent") == intent
        checks.append({"name": f"intent={intent}", "ok": ok, "detail": str(body.get("intent"))})

    if tools := expect.get("tools_contains"):
        used = body.get("tools_used") or []
        if isinstance(tools, list):
            ok = all(t in used for t in tools)
        else:
            ok = tools in used
        checks.append({"name": f"tools_contains={tools}", "ok": ok, "detail": str(used)})

    if tools_any := expect.get("tools_any"):
        used = body.get("tools_used") or []
        ok = any(t in used for t in tools_any)
        checks.append({"name": f"tools_any={tools_any}", "ok": ok, "detail": str(used)})

    if cites_any := expect.get("citations_any"):
        ok = any(token.lower() in cites for token in cites_any)
        checks.append({"name": f"citations_any={cites_any}", "ok": ok, "detail": cites[:120]})

    for token in expect.get("reply_contains", []):
        ok = token.lower() in reply
        checks.append({"name": f"reply_contains={token}", "ok": ok, "detail": reply[:120]})

    if contains_any := expect.get("reply_contains_any"):
        ok = any(token.lower() in reply for token in contains_any)
        checks.append({"name": f"reply_contains_any={contains_any}", "ok": ok, "detail": reply[:120]})

    for token in expect.get("reply_not_contains", []):
        ok = token.lower() not in reply and token.lower() not in cites
        checks.append({"name": f"reply_not_contains={token}", "ok": ok, "detail": reply[:120]})

    if max_len := expect.get("max_reply_length"):
        ok = len(body.get("reply") or "") <= int(max_len)
        checks.append({"name": f"max_reply_length={max_len}", "ok": ok, "detail": str(len(body.get("reply") or ""))})

    if expect.get("reply_not_contains") is None and '"id":' not in expect.get("reply_not_contains", []):
        if re.search(r'\{\s*"id"\s*:', body.get("reply") or ""):
            checks.append({"name": "no_json_leak", "ok": False, "detail": "JSON object in reply"})

    return checks


def build_report(
    results: dict[str, list[dict[str, Any]]],
    dialogues: list[dict[str, Any]],
    source_note: str,
) -> str:
    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    total_turns = sum(len(turns) for turns in results.values())
    passed_turns = sum(1 for turns in results.values() for t in turns if t["passed"])
    failed = [
        (script_id, idx + 1, turn)
        for script_id, turns in results.items()
        for idx, turn in enumerate(turns)
        if not turn["passed"]
    ]

    lines = [
        "# Consult Dialogue Simulation Report",
        "",
        f"> Generated: {generated} · synthetic demo data · API v0.5.13",
        "",
        f"Multi-turn buyer consultation scripts. Source: {source_note}.",
        "",
        "## Summary",
        "",
        f"- Scripts: **{len(dialogues)}** · Turns: **{total_turns}** · Passed: **{passed_turns}/{total_turns}**",
        "",
        "| Script | Turns | Pass | Description |",
        "|--------|-------|------|-------------|",
    ]

    id_to_desc = {d["id"]: d.get("description", "") for d in dialogues}
    for script_id, turns in results.items():
        ok_count = sum(1 for t in turns if t["passed"])
        lines.append(
            f"| `{script_id}` | {len(turns)} | {ok_count}/{len(turns)} | {id_to_desc.get(script_id, '')} |"
        )

    if failed:
        lines.extend(["", "## Failed turns", ""])
        for script_id, turn_no, turn in failed:
            lines.append(f"### `{script_id}` turn {turn_no}")
            lines.append(f"- User: {turn['user']!r}")
            lines.append(f"- Intent: {turn['response'].get('intent')} · mode: {turn['response'].get('retrieval_mode')}")
            for check in turn["checks"]:
                if not check["ok"]:
                    lines.append(f"- FAIL `{check['name']}` — {check['detail']}")
            excerpt = (turn["response"].get("reply") or "")[:400]
            lines.append(f"- Reply excerpt: {excerpt!r}")
            lines.append("")

    for script in dialogues:
        script_id = script["id"]
        turns = results.get(script_id, [])
        lines.extend(["", f"## `{script_id}`", "", f"_{script.get('description', '')}_", ""])
        for idx, turn in enumerate(turns, start=1):
            body = turn["response"]
            status = "PASS" if turn["passed"] else "FAIL"
            lines.append(f"### Turn {idx} — {status}")
            lines.append(f"- User: {turn['user']!r}")
            lines.append(f"- Intent: `{body.get('intent')}` · mode: `{body.get('retrieval_mode')}`")
            lines.append(f"- Tools: `{body.get('tools_used')}`")
            lines.append(f"- Reply: {(body.get('reply') or '')[:500]}")
            lines.append("")

    lines.extend(
        [
            "## Recommended tuning",
            "",
            "- Prefer `consult_kb` RAG filter for project_faq (no synthetic project JSON in replies).",
            "- Villa requests → honest Bangkok luxury condo inventory (Landmark Sukhumvit), not Phuket villas.",
            "- Session-aware retrieval query for follow-ups («what do you have and where?»).",
            "- WhatsApp: `_sanitize_reply()` max 1200 chars, no JSON leak.",
            "",
            "## Related",
            "",
            "- [`CONSULT_KNOWLEDGE_DEMO.md`](CONSULT_KNOWLEDGE_DEMO.md)",
            "- [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CONSULT_DIALOGUE_SIMULATION_REPORT.md")
    parser.add_argument("--offline", action="store_true", help="In-process with LLM mocked (template path)")
    parser.add_argument(
        "--api-url",
        default="",
        help="Live API base URL (e.g. http://localhost:8080) — uses LM Studio if configured",
    )
    args = parser.parse_args()

    dialogues = _load_matrix()
    if args.api_url.strip():
        results = _run_api(args.api_url.strip(), dialogues)
        source = f"`scripts/run_consult_dialogue_matrix.py --api-url {args.api_url.strip()}`"
    else:
        results = _run_offline(dialogues)
        source = "`scripts/run_consult_dialogue_matrix.py --offline`"

    output = ROOT / "docs" / "CONSULT_DIALOGUE_SIMULATION_REPORT.md"
    output.write_text(build_report(results, dialogues, source), encoding="utf-8")
    passed = sum(1 for turns in results.values() for t in turns if t["passed"])
    total = sum(len(turns) for turns in results.values())
    print(f"Wrote {output} ({passed}/{total} turns passed)")
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
