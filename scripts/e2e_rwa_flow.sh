#!/usr/bin/env bash
# End-to-end RWA settlement flow against the local dev chain.
#
# Flow:
#   1. Ensure ./scripts/dev-chain.sh is running.
#   2. Ensure contracts are deployed (./scripts/deploy-contracts.sh).
#   3. Start the FastAPI attester (if not running) with .dev-chain.state env.
#   4. Mint Mock USDC to the buyer EOA.
#   5. Buyer approves SettlementEscrow.
#   6. Buyer deposits into SettlementEscrow under a deterministic dealId.
#   7. Backend attester signs and broadcasts the EAS SettlementApproval.
#   8. Anyone calls SettlementEscrow.release(dealId, attestationUid).
#   9. Print payee balance + attestation explorer link.
#
# Idempotent across restarts by clearing api pid/log and using a new dealId
# each run (timestamp salt). Aborts on the first failure.

set -euo pipefail

# shellcheck disable=SC2155
export PATH="$HOME/.foundry/bin:$PATH"

STATE_FILE="${ATTESTRWA_STATE_FILE:-.dev-chain.state}"
API_LOG=/tmp/attestrwa-api.log
API_PID_FILE=/tmp/attestrwa-api.pid
API_HOST=127.0.0.1
API_PORT=${ATTESTRWA_API_PORT:-8080}

# Anvil default account #1 = buyer (public test key, never use on mainnet)
BUYER_ADDRESS=0x70997970C51812dc3A010C7d01b50e0d17dc79C8
BUYER_PK=0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d

# Demo payee (Bangkok Landmark Group authorized) = Anvil acc 6
PAYEE_ADDRESS=0x976EA74026E726554dB657fA54763abd0C3a0aa9

AMOUNT_BASE_UNITS=580000000 # 580 USDC

log() { printf '\n\033[1;36m[e2e]\033[0m %s\n' "$*" >&2; }
ok()  { printf '\033[1;32m[ok]\033[0m  %s\n' "$*" >&2; }
err() { printf '\033[1;31m[err]\033[0m %s\n' "$*" >&2; }

require_state() {
  if [ ! -f "$STATE_FILE" ]; then
    err "$STATE_FILE not found. Run ./scripts/dev-chain.sh first."
    exit 1
  fi
  # shellcheck disable=SC1090
  source "$STATE_FILE"
  : "${DEV_RPC_URL:?missing in state}"
  : "${EAS_SCHEMA_UID_SETTLEMENT_APPROVAL:?missing in state}"
  : "${ATTESTER_ADDRESS:?missing in state}"
  : "${ATTESTER_PRIVATE_KEY:?missing in state}"
  : "${MOCK_USDC_ADDRESS:?run ./scripts/deploy-contracts.sh first}"
  : "${SETTLEMENT_ESCROW_ADDRESS:?run ./scripts/deploy-contracts.sh first}"
}

ensure_api_up() {
  if curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
    ok "FastAPI already up on :${API_PORT}"
    return 0
  fi
  log "Starting FastAPI attester on :${API_PORT} (log: ${API_LOG})…"
  (
    cd apps/api
    DEV_RPC_URL="$DEV_RPC_URL" \
    EAS_SCHEMA_UID_SETTLEMENT_APPROVAL="$EAS_SCHEMA_UID_SETTLEMENT_APPROVAL" \
    ATTESTER_ADDRESS="$ATTESTER_ADDRESS" \
    ATTESTER_PRIVATE_KEY="$ATTESTER_PRIVATE_KEY" \
    EAS_ADDRESS="${EAS_ADDRESS:-0x4200000000000000000000000000000000000021}" \
    DEV_CHAIN_ID="${DEV_CHAIN_ID:-84532}" \
    nohup uv run uvicorn app.main:app --app-dir src --host "$API_HOST" --port "$API_PORT" \
      >"$API_LOG" 2>&1 &
    echo $! > "$API_PID_FILE"
  )
  for _ in $(seq 1 30); do
    if curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
      ok "FastAPI healthy (pid $(cat "$API_PID_FILE"))"
      return 0
    fi
    sleep 1
  done
  err "FastAPI did not become healthy. Last log:"
  tail -20 "$API_LOG" >&2
  exit 1
}

run() {
  require_state
  ensure_api_up

  local salt="$(date +%s%N)"
  local DEAL_ID="0x$(printf 'attestrwa-e2e-%s' "$salt" | shasum -a 256 | awk '{print $1}')"
  local DEADLINE=$(( $(date +%s) + 86400 ))

  log "Deal id (this run): $DEAL_ID"

  log "1) Mint $AMOUNT_BASE_UNITS mUSDC to buyer $BUYER_ADDRESS"
  cast send "$MOCK_USDC_ADDRESS" "mint(address,uint256)" \
      "$BUYER_ADDRESS" "$AMOUNT_BASE_UNITS" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$ATTESTER_PRIVATE_KEY" >/dev/null
  ok "minted"

  log "2) Buyer approves SettlementEscrow"
  cast send "$MOCK_USDC_ADDRESS" "approve(address,uint256)" \
      "$SETTLEMENT_ESCROW_ADDRESS" "$AMOUNT_BASE_UNITS" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "approve"

  log "3) Buyer deposits to escrow"
  cast send "$SETTLEMENT_ESCROW_ADDRESS" \
      "deposit(bytes32,address,address,uint256,uint64)" \
      "$DEAL_ID" "$PAYEE_ADDRESS" "$MOCK_USDC_ADDRESS" "$AMOUNT_BASE_UNITS" "$DEADLINE" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "deposit"

  log "4) Backend attester decides + signs + broadcasts EAS attestation"
  local body
  body=$(cat <<EOF
{
  "deal_id": "$DEAL_ID",
  "buyer_wallet": "$BUYER_ADDRESS",
  "payee_wallet": "$PAYEE_ADDRESS",
  "token_address": "$MOCK_USDC_ADDRESS",
  "amount_base_units": $AMOUNT_BASE_UNITS,
  "developer_id": "developer-bangkok-landmark",
  "jurisdiction": "TH",
  "buyer_kyc_tier": 3,
  "expires_in_seconds": 86400
}
EOF
)
  local attest_resp
  attest_resp=$(curl -fsS -X POST \
      "http://${API_HOST}:${API_PORT}/attest/settlement" \
      -H 'Content-Type: application/json' \
      -d "$body")
  echo "$attest_resp" | python3 -m json.tool >&2

  local decision uid txhash
  decision=$(echo "$attest_resp" | python3 -c "import sys,json; print(json.load(sys.stdin)['decision'])")
  uid=$(echo "$attest_resp" | python3 -c "import sys,json; v=json.load(sys.stdin).get('attestation_uid'); print(v or '')")
  txhash=$(echo "$attest_resp" | python3 -c "import sys,json; v=json.load(sys.stdin).get('tx_hash'); print(v or '')")

  if [ "$decision" != "approve" ]; then
    err "Attester decision was '$decision' — flow expected 'approve'"
    exit 1
  fi
  if [ -z "$uid" ]; then
    err "Attester did not submit attestation on-chain (uid empty). Check $API_LOG"
    exit 1
  fi
  ok "Attestation UID: $uid (tx $txhash)"

  log "5) Release escrow to payee using attestation"
  cast send "$SETTLEMENT_ESCROW_ADDRESS" "release(bytes32,bytes32)" \
      "$DEAL_ID" "$uid" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "release"

  local payee_balance
  payee_balance=$(cast call "$MOCK_USDC_ADDRESS" "balanceOf(address)(uint256)" \
      "$PAYEE_ADDRESS" --rpc-url "$DEV_RPC_URL")
  ok "Payee balance now: $payee_balance base units"

  cat <<SUMMARY

================================================================
AttestRWA end-to-end happy-path settlement: SUCCESS
================================================================
  Deal id           : $DEAL_ID
  Buyer             : $BUYER_ADDRESS
  Payee             : $PAYEE_ADDRESS
  Token (MockUSDC)  : $MOCK_USDC_ADDRESS
  Escrow            : $SETTLEMENT_ESCROW_ADDRESS
  Amount (uUSDC)    : $AMOUNT_BASE_UNITS
  Attestation UID   : $uid
  Tx hash (attest)  : $txhash
  Payee final bal   : $payee_balance
================================================================

SUMMARY
}

run "$@"
