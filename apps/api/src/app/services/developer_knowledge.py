from typing import Any

from app.services.data_loader import load_json

PRIOR_ART_REFERENCE = "https://github.com/FUYOH666/realestate-agent-platform"
DEFAULT_FEED = "developers/siam-riverside-feed.json"
LANDMARK_FEED = "developers/bangkok-landmark-feed.json"
SHADOW_FEED = "developers/shadow-bay-feed.json"


def load_developer_feed(feed_path: str = DEFAULT_FEED) -> dict[str, Any]:
    return load_json(feed_path)


def _feed_snapshot(feed: dict[str, Any]) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "last_updated": feed.get("last_updated"),
        "authorized_payees": feed.get("authorized_payees", []),
        "units_available_count": len(feed.get("units_available", [])),
        "payment_terms": feed.get("payment_terms", {}),
        "installment_schedule_summary": feed.get("installment_schedule_summary", ""),
    }
    if feed.get("units_available"):
        snapshot["sample_unit"] = feed["units_available"][0]
    for key in (
        "permit_status",
        "eia_status",
        "sales_status",
        "construction_permit_issued",
        "license_sales_entity",
        "network_status",
        "reputation_tier",
    ):
        if key in feed:
            snapshot[key] = feed[key]
    return snapshot


def build_developer_knowledge_hub(
    case: dict[str, Any],
    feed_path: str = DEFAULT_FEED,
) -> dict[str, Any]:
    feed = load_developer_feed(feed_path)
    authorized_payees = feed.get("authorized_payees", [])
    instruction_payee = case.get("payment_instruction_payee", "")
    authorized_payee = authorized_payees[0] if authorized_payees else ""

    if not authorized_payees:
        mismatch_status = "no_authorized_payee_in_feed"
    elif instruction_payee in authorized_payees:
        mismatch_status = "aligned"
    else:
        mismatch_status = "mismatch_detected"

    return {
        "data_classification": "synthetic_demo_data",
        "module": "developer_knowledge_hub",
        "vision_note": "Strategic extension teaser. Multi-channel agents not live in hackathon MVP.",
        "developer": feed["developer_name"],
        "project": feed["project_name"],
        "source_of_truth": feed["source_of_truth"],
        "feed_snapshot": _feed_snapshot(feed),
        "knowledge_vs_agent_gap": {
            "agent_claimed_payee": instruction_payee,
            "developer_authorized_payee": authorized_payee,
            "status": mismatch_status,
            "note": _gap_note(mismatch_status, feed),
        },
        "consumption_model": "verified_agencies_read_only_from_hub",
        "channel_roadmap": [
            {"id": "whatsapp", "label": "WhatsApp", "status": "roadmap"},
            {"id": "telegram", "label": "Telegram", "status": "roadmap"},
            {"id": "email", "label": "Email", "status": "roadmap"},
            {"id": "voice_tts", "label": "Voice assistant (TTS)", "status": "roadmap"},
        ],
        "ai_stack": {
            "retrieval": "Qdrant + BGE-M3 (demo) — Qwen-class at scale",
            "generation": "schema-bound LLM via LM Studio (demo) — vLLM gateway at scale",
            "fallback": "deterministic rules when services unavailable",
        },
        "prior_art": {
            "project": "realestate-agent-platform",
            "reference_url": PRIOR_ART_REFERENCE,
            "note": "Archived reference for multi-channel DomainPack agent architecture.",
        },
        "downstream_link": "Property Shield compares agent instructions against this feed before settlement routing.",
        "pitch_line": (
            "Discovery agents distort facts because they have no source of truth. "
            "The developer does. Bankable Property OS connects verified developer knowledge to bank-grade settlement rails."
        ),
    }


def _gap_note(mismatch_status: str, feed: dict[str, Any]) -> str:
    if mismatch_status == "no_authorized_payee_in_feed":
        return (
            "Developer is off-network or prelaunch feed has no authorized payees. "
            "Deposits must not move until permit and payee authority are verified."
        )
    if mismatch_status == "mismatch_detected":
        return "Agent payment instruction does not match developer authorized payee."
    return "Agent instruction matches developer feed."


def build_feed_summary(feed_path: str) -> dict[str, Any]:
    feed = load_developer_feed(feed_path)
    return {
        "developer": feed["developer_name"],
        "project": feed["project_name"],
        "source_of_truth": feed["source_of_truth"],
        "feed_snapshot": _feed_snapshot(feed),
    }
