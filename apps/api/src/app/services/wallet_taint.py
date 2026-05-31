"""Wallet taint classification for AttestRWA.

Returns a capital class for a buyer wallet: 0 (green), 1 (amber), or 2 (red).
Production uses Chainalysis / TRM Labs; demo uses a deterministic synthetic map.

Providers implement `TaintProvider` — select via `ATTESTRWA_TAINT_PROVIDER` env.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

CAPITAL_CLASS_GREEN = 0
CAPITAL_CLASS_AMBER = 1
CAPITAL_CLASS_RED = 2

# Mapping of synthetic mixer / sanction signals to wallet addresses.
_TAINT_SIGNALS: dict[str, dict[str, str]] = {
    "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f": {
        "tornado_cash_2_hop": "Wallet shows two-hop interaction with sanctioned mixer",
        "wallet_age_days_3": "Wallet less than 7 days old",
    },
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
    provider: str = "mock"
    error: str | None = None


@runtime_checkable
class TaintProvider(Protocol):
    """Pluggable wallet taint backend."""

    name: str

    def classify(self, wallet: str) -> TaintReport: ...


class MockTaintProvider:
    """Deterministic demo classifier keyed off synthetic wallet addresses."""

    name = "mock"

    def classify(self, wallet: str) -> TaintReport:
        if not wallet:
            return TaintReport(wallet, CAPITAL_CLASS_GREEN, [], "empty wallet", provider=self.name)

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
                provider=self.name,
            )

        signals = list(direct.keys())
        explanation = "; ".join(direct.values())

        if any(s in {"tornado_cash_2_hop", "sanction_list_hit"} for s in signals):
            return TaintReport(wallet, CAPITAL_CLASS_RED, signals, explanation, provider=self.name)

        return TaintReport(wallet, CAPITAL_CLASS_AMBER, signals, explanation, provider=self.name)


class ChainalysisStubProvider:
    """Placeholder for Chainalysis API integration.

    Set `ATTESTRWA_TAINT_PROVIDER=chainalysis_stub` to exercise the wiring.
    Returns structured errors until `ATTESTRWA_CHAINALYSIS_API_KEY` is configured.
    """

    name = "chainalysis_stub"

    def classify(self, wallet: str) -> TaintReport:
        api_key = os.getenv("ATTESTRWA_CHAINALYSIS_API_KEY", "").strip()
        if not api_key:
            return TaintReport(
                wallet=wallet,
                capital_class=CAPITAL_CLASS_GREEN,
                signals=["chainalysis_not_configured"],
                explanation="Chainalysis stub: API key missing — defaulting green for demo",
                provider=self.name,
                error="ATTESTRWA_CHAINALYSIS_API_KEY not set",
            )
        return TaintReport(
            wallet=wallet,
            capital_class=CAPITAL_CLASS_GREEN,
            signals=["chainalysis_stub_pending"],
            explanation="Chainalysis stub: API key present but HTTP client not implemented",
            provider=self.name,
            error="ChainalysisStubProvider: implement HTTP client before production use",
        )


_PROVIDERS: dict[str, type[TaintProvider]] = {
    "mock": MockTaintProvider,
    "chainalysis_stub": ChainalysisStubProvider,
}


def get_taint_provider() -> TaintProvider:
    """Return the configured taint provider (default: mock)."""
    key = os.getenv("ATTESTRWA_TAINT_PROVIDER", "mock").strip().lower()
    cls = _PROVIDERS.get(key, MockTaintProvider)
    return cls()


def classify_wallet(wallet: str) -> TaintReport:
    """Classify wallet via the active provider."""
    return get_taint_provider().classify(wallet)
