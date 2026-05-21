"""Web3 client for EAS (Ethereum Attestation Service) on Base Sepolia / fork.

Wraps the minimal EAS surface AttestRWA needs:

- `attest(request)`           — submit an on-chain attestation
- `get_attestation(uid)`      — read an attestation
- `health()`                  — chain reachability + attester balance

The client is intentionally thin: it does not pretend to be the official
EAS SDK. It is built on the official EAS contract ABI fragments (`attest`,
`getAttestation`, `Attested` event) and on canonical addresses pinned at
deploy time.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Any

from eth_abi.abi import encode as abi_encode
from eth_account import Account
from web3 import Web3
from web3.exceptions import ContractLogicError

logger = logging.getLogger(__name__)

# Canonical EAS contract on Base mainnet, Base Sepolia, Optimism, and any
# Base fork. Same address inside the dev Anvil fork.
EAS_CONTRACT_ADDRESS = "0x4200000000000000000000000000000000000021"

# Minimal ABI: only the methods AttestRWA invokes.
EAS_ABI: list[dict[str, Any]] = [
    {
        "type": "function",
        "stateMutability": "payable",
        "name": "attest",
        "inputs": [
            {
                "name": "request",
                "type": "tuple",
                "components": [
                    {"name": "schema", "type": "bytes32"},
                    {
                        "name": "data",
                        "type": "tuple",
                        "components": [
                            {"name": "recipient", "type": "address"},
                            {"name": "expirationTime", "type": "uint64"},
                            {"name": "revocable", "type": "bool"},
                            {"name": "refUID", "type": "bytes32"},
                            {"name": "data", "type": "bytes"},
                            {"name": "value", "type": "uint256"},
                        ],
                    },
                ],
            },
        ],
        "outputs": [{"name": "", "type": "bytes32"}],
    },
    {
        "type": "function",
        "stateMutability": "view",
        "name": "getAttestation",
        "inputs": [{"name": "uid", "type": "bytes32"}],
        "outputs": [
            {
                "name": "",
                "type": "tuple",
                "components": [
                    {"name": "uid", "type": "bytes32"},
                    {"name": "schema", "type": "bytes32"},
                    {"name": "time", "type": "uint64"},
                    {"name": "expirationTime", "type": "uint64"},
                    {"name": "revocationTime", "type": "uint64"},
                    {"name": "refUID", "type": "bytes32"},
                    {"name": "recipient", "type": "address"},
                    {"name": "attester", "type": "address"},
                    {"name": "revocable", "type": "bool"},
                    {"name": "data", "type": "bytes"},
                ],
            }
        ],
    },
    {
        "type": "event",
        "name": "Attested",
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "recipient", "type": "address"},
            {"indexed": True, "name": "attester", "type": "address"},
            {"indexed": False, "name": "uid", "type": "bytes32"},
            {"indexed": True, "name": "schemaUID", "type": "bytes32"},
        ],
    },
]

# SettlementApproval schema field types (must match the schema string).
SETTLEMENT_APPROVAL_TYPES = (
    "bytes32",   # dealId
    "address",   # attester
    "address",   # payeeAddress
    "address",   # tokenAddress
    "uint256",   # amount
    "uint8",     # capitalClass
    "bytes32",   # evidenceHash
    "string",    # jurisdiction
    "uint64",    # expiresAt
    "bool",      # payeeVerified
)


@dataclass(slots=True, frozen=True)
class SettlementApprovalPayload:
    """Strongly-typed payload that maps to the SettlementApproval schema."""

    deal_id: bytes
    attester: str
    payee_address: str
    token_address: str
    amount: int
    capital_class: int
    evidence_hash: bytes
    jurisdiction: str
    expires_at: int
    payee_verified: bool

    def encode(self) -> bytes:
        """ABI-encode the payload into a bytes blob suitable for EAS `data`."""
        return abi_encode(
            list(SETTLEMENT_APPROVAL_TYPES),
            [
                self.deal_id,
                Web3.to_checksum_address(self.attester),
                Web3.to_checksum_address(self.payee_address),
                Web3.to_checksum_address(self.token_address),
                int(self.amount),
                int(self.capital_class),
                self.evidence_hash,
                self.jurisdiction,
                int(self.expires_at),
                bool(self.payee_verified),
            ],
        )


@dataclass(slots=True)
class EASConfig:
    """Runtime parameters for the EAS client."""

    rpc_url: str
    schema_uid: str
    attester_private_key: str
    eas_address: str = EAS_CONTRACT_ADDRESS
    chain_id: int = 84532
    request_timeout_s: int = 30


@dataclass(slots=True, frozen=True)
class AttestationResult:
    """Successful attestation receipt."""

    uid: str
    tx_hash: str
    block_number: int
    gas_used: int


def _config_from_env() -> EASConfig:
    return EASConfig(
        rpc_url=os.getenv("DEV_RPC_URL", "http://127.0.0.1:8545"),
        schema_uid=os.environ["EAS_SCHEMA_UID_SETTLEMENT_APPROVAL"],
        attester_private_key=os.environ["ATTESTER_PRIVATE_KEY"],
        eas_address=os.getenv("EAS_ADDRESS", EAS_CONTRACT_ADDRESS),
        chain_id=int(os.getenv("DEV_CHAIN_ID", "84532")),
    )


class EASClient:
    """Thin wrapper around the EAS contract for AttestRWA.

    Builds a `Web3` instance lazily; raises clear errors when env is missing.
    """

    def __init__(self, config: EASConfig | None = None) -> None:
        self.config = config or _config_from_env()
        self._w3: Web3 | None = None

    # ---- low-level connectivity --------------------------------------------

    @property
    def w3(self) -> Web3:
        if self._w3 is None:
            self._w3 = Web3(Web3.HTTPProvider(self.config.rpc_url, request_kwargs={"timeout": self.config.request_timeout_s}))
        return self._w3

    @property
    def attester_address(self) -> str:
        return Account.from_key(self.config.attester_private_key).address

    @property
    def contract(self):
        return self.w3.eth.contract(
            address=Web3.to_checksum_address(self.config.eas_address),
            abi=EAS_ABI,
        )

    # ---- public API --------------------------------------------------------

    def health(self) -> dict[str, Any]:
        """Quick health check used by `/attest/healthz`."""
        try:
            reachable = self.w3.is_connected()
            block = self.w3.eth.block_number if reachable else None
            balance_wei = self.w3.eth.get_balance(self.attester_address) if reachable else 0
        except Exception as exc:
            return {
                "status": "down",
                "service": "attestrwa-attester",
                "error": f"{type(exc).__name__}: {exc}",
            }
        return {
            "status": "ok" if reachable else "down",
            "service": "attestrwa-attester",
            "rpc_url": self.config.rpc_url,
            "chain_id": self.config.chain_id,
            "block_number": block,
            "eas_address": self.config.eas_address,
            "schema_uid": self.config.schema_uid,
            "attester_address": self.attester_address,
            "attester_balance_eth": float(self.w3.from_wei(balance_wei, "ether")) if reachable else 0.0,
        }

    def attest(
        self,
        payload: SettlementApprovalPayload,
        *,
        revocable: bool = True,
        recipient: str = "0x0000000000000000000000000000000000000000",
        expiration_time: int | None = None,
    ) -> AttestationResult:
        """Submit an attestation on-chain.

        Raises `ContractLogicError` if the EAS contract reverts (e.g. when the
        schema UID is wrong). Network errors propagate.
        """
        encoded_data = payload.encode()
        if expiration_time is None:
            expiration_time = payload.expires_at

        request = (
            Web3.to_bytes(hexstr=self.config.schema_uid),
            (
                Web3.to_checksum_address(recipient),
                int(expiration_time),
                bool(revocable),
                b"\x00" * 32,
                encoded_data,
                0,
            ),
        )

        nonce = self.w3.eth.get_transaction_count(self.attester_address)
        tx = self.contract.functions.attest(request).build_transaction(
            {
                "from": self.attester_address,
                "nonce": nonce,
                "chainId": self.config.chain_id,
                "value": 0,
                "gas": 600_000,
            }
        )
        signed = self.w3.eth.account.sign_transaction(tx, self.config.attester_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=self.config.request_timeout_s)
        if receipt.status != 1:
            raise ContractLogicError(f"EAS.attest reverted (txHash={tx_hash.hex()})")

        attested_event = self.contract.events.Attested().process_receipt(receipt)
        if not attested_event:
            raise RuntimeError("EAS.attest receipt missing Attested event")

        uid = attested_event[0]["args"]["uid"]
        logger.info(
            "EAS attest tx=%s uid=%s block=%s gas=%s",
            tx_hash.hex(),
            uid.hex(),
            receipt.blockNumber,
            receipt.gasUsed,
        )
        return AttestationResult(
            uid="0x" + uid.hex(),
            tx_hash="0x" + tx_hash.hex(),
            block_number=int(receipt.blockNumber),
            gas_used=int(receipt.gasUsed),
        )

    def get_attestation(self, uid: str) -> dict[str, Any]:
        """Read an attestation back from the chain."""
        raw = self.contract.functions.getAttestation(Web3.to_bytes(hexstr=uid)).call()
        # Tuple order matches the Attestation struct.
        return {
            "uid": "0x" + raw[0].hex(),
            "schema": "0x" + raw[1].hex(),
            "time": int(raw[2]),
            "expirationTime": int(raw[3]),
            "revocationTime": int(raw[4]),
            "refUID": "0x" + raw[5].hex(),
            "recipient": raw[6],
            "attester": raw[7],
            "revocable": bool(raw[8]),
            "data": "0x" + raw[9].hex(),
        }


def build_default_evidence_hash(*parts: str) -> bytes:
    """Helper: deterministic evidence hash from a list of citation strings."""
    canonical = "\n".join(parts).encode("utf-8")
    return Web3.keccak(canonical)


def current_expiration(seconds_from_now: int = 86_400) -> int:
    """Helper: default expiration `seconds_from_now` from current Unix time."""
    return int(time.time()) + int(seconds_from_now)
