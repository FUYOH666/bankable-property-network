from typing import Any


def classify_capital_sources(sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    for source in sources:
        source_id = str(source["id"])
        kind = source.get("kind")

        if kind == "bank_transfer" and source.get("proof"):
            status = "green"
            reason = "Bank transfer has clear source-of-funds evidence."
        elif kind == "stablecoin" and source.get("wallet_summary") == "explainable":
            status = "amber"
            reason = "Stablecoin funds may be bankable after wallet and source documentation review."
        else:
            status = "red"
            reason = "Funds lack a bank-verifiable counterparty or source-of-funds trail."

        result[source_id] = {
            "status": status,
            "kind": kind,
            "amount": source.get("amount"),
            "currency": source.get("currency"),
            "reason": reason,
        }

    return result
