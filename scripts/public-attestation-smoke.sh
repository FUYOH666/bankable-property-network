#!/usr/bin/env bash
# One happy-path attestation on public Base Sepolia via the attester API.
#
# Prerequisites:
#   ./scripts/deploy-public-testnet.sh completed
#   FastAPI running with PROD RPC env (or source .public-testnet.state)
#
# Prints attestation UID for README / Dune.

set -euo pipefail

export PATH="$HOME/.foundry/bin:$PATH"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

STATE_FILE="${ATTESTRWA_PUBLIC_STATE_FILE:-.public-testnet.state}"
API_PORT=${ATTESTRWA_API_PORT:-8080}
API_HOST=${ATTESTRWA_API_HOST:-127.0.0.1}

if [ -f "$STATE_FILE" ]; then
  # shellcheck disable=SC1090
  set -a
  source "$STATE_FILE"
  set +a
  export DEV_RPC_URL
  export ATTESTER_PRIVATE_KEY
  export ATTESTER_ADDRESS
  export EAS_SCHEMA_UID_SETTLEMENT_APPROVAL
fi

log() { printf '[public-smoke] %s\n' "$*" >&2; }

if ! curl -sf "http://${API_HOST}:${API_PORT}/attest/healthz" >/dev/null 2>&1; then
  log "Starting attester API in background…"
  (cd apps/api && uv run uvicorn app.main:app --app-dir src --host "$API_HOST" --port "$API_PORT") &
  sleep 3
fi

DEAL_ID="0x$(openssl rand -hex 32)"

BODY=$(cat <<JSON
{
  "deal_id": "$DEAL_ID",
  "buyer_wallet": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
  "payee_wallet": "0x976EA74026E726554dB657fA54763abd0C3a0aa9",
  "token_address": "${MOCK_USDC_ADDRESS:-0xeba5CEc9257045Df0B44eA784F9a7Fa07DeeF6d4}",
  "amount_base_units": 580000000,
  "developer_id": "developer-bangkok-landmark",
  "jurisdiction": "TH",
  "buyer_kyc_tier": 3
}
JSON
)

log "POST /attest/settlement deal_id=$DEAL_ID"
RESP=$(curl -sf -X POST "http://${API_HOST}:${API_PORT}/attest/settlement" \
  -H "Content-Type: application/json" \
  -d "$BODY")

echo "$RESP" | python3 -m json.tool 2>/dev/null || echo "$RESP"

UID=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('attestation_uid') or '')" 2>/dev/null || true)

if [ -n "$UID" ] && [ "$UID" != "None" ]; then
  log "Attestation UID: $UID"
  log "EAS Scan: https://base-sepolia.easscan.org/attestation/view/${UID#0x}"
else
  log "No on-chain UID (RPC unreachable or attest skipped) — decision payload still valid for demo."
fi
