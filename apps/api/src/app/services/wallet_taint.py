"""Mock wallet taint classifier for AttestRWA.

Returns a capital class for a buyer wallet: 0 (green), 1 (amber), or 2 (red).
In production this is backed by a real Chainalysis / TRM Labs feed; in the
hackathon demo we use a deterministic synthetic list keyed off the demo
wallet addresses in `data/synthetic/rwa/wallets.json`.

The classifier is intentionally pure and side-effect-free so the attester
service can reason about it cheaply.
"""

from __future__ import annotations

from dataclasses import dataclass

CAPITAL_CLASS_GREEN = 0
CAPITAL_CLASS_AMBER = 1
CAPITAL_CLASS_RED = 2

# Mapping of synthetic mixer / sanction signals to wallet addresses.
# Production replaces this with live Chainalysis / TRM Labs API. The
# addresses listed here mirror data/synthetic/rwa/wallets.json.
_TAINT_SIGNALS: dict[str, dict[str, str]] = {
    "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f": {
        "tornado_cash_2_hop": "Wallet shows two-hop interaction with sanctioned mixer",
        "wallet_age_days_3": "Wallet less than 7 days old",
    },
    # Reserved slot for amber-class examples
    "0x00000000000000000000000000000000000000a1": {
        "stale_inactive_5y": "No outgoing tx in 5 years — heightened review",
    },
}


@dataclass(slots=True)
class TaintReport:
    """Result of a wallet classification."""

    wallet: str
    capital_class: int  # 0 green, 1 amber, 2 red
    signals: list[str]
    explanation: str


def _normalize(wallet: str) -> str:
    """Normalize a wallet address to checksummed lower-then-original casing.

    For demo we store addresses with their canonical (case-sensitive)
    representation; production would use the eth_utils checksum. Two simple
    checks here: same-case match, then lowercase fallback.
    """
    return wallet


def classify_wallet(wallet: str) -> TaintReport:
    """Return a `TaintReport` for the given wallet address.

    Lookup is exact-match against the static map and then a case-insensitive
    fallback. Unknown wallets default to green.
    """
    if not wallet:
        return TaintReport(wallet, CAPITAL_CLASS_GREEN, [], "empty wallet")

    direct = _TAINT_SIGNALS.get(wallet)
    if direct is None:
        wallet_lower = wallet.lower()
        for known_wallet, signals in _TAINT_SIGNALS.items():
            if known_wallet.lower() == wallet_lower:
                direct = signals
                break

    if not direct:
        return TaintReport(
            wallet=wallet,
            capital_class=CAPITAL_CLASS_GREEN,
            signals=[],
            explanation="no taint signals; wallet classified green",
        )

    signals = list(direct.keys())
    explanation = "; ".join(direct.values())

    if any(s in {"tornado_cash_2_hop", "sanction_list_hit"} for s in signals):
        return TaintReport(wallet, CAPITAL_CLASS_RED, signals, explanation)

    return TaintReport(wallet, CAPITAL_CLASS_AMBER, signals, explanation)
