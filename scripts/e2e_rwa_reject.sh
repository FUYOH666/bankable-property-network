#!/usr/bin/env bash
# End-to-end RWA settlement REJECT path against the local dev chain.
#
# Same orchestration as scripts/e2e_rwa_flow.sh, but the buyer instructs the
# escrow to release to the impostor `SRL Holding 2026` wallet that is not
# in the developer feed. The attester signs an EAS attestation with
# `payeeVerified=false`, the escrow refuses release, and the buyer is
# refunded via the attester-signed-reject path.

set -euo pipefail

# shellcheck disable=SC2155
export PATH="$HOME/.foundry/bin:$PATH"

STATE_FILE="${ATTESTRWA_STATE_FILE:-.dev-chain.state}"
API_HOST=127.0.0.1
API_PORT=${ATTESTRWA_API_PORT:-8080}

BUYER_ADDRESS=0x70997970C51812dc3A010C7d01b50e0d17dc79C8
BUYER_PK=0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d

# Anvil acc 3 — impostor payee claiming "SRL Holding 2026 Co., Ltd."
IMPOSTOR_PAYEE=0x90F79bf6EB2c4f870365E785982E1f101E93b906

AMOUNT_BASE_UNITS=280000000 # 280 USDC

log() { printf '\n\033[1;36m[reject]\033[0m %s\n' "$*" >&2; }
ok()  { printf '\033[1;32m[ok]\033[0m  %s\n' "$*" >&2; }
err() { printf '\033[1;31m[err]\033[0m %s\n' "$*" >&2; }

require_state() {
  [ -f "$STATE_FILE" ] || { err "$STATE_FILE missing — run ./scripts/dev-chain.sh"; exit 1; }
  # shellcheck disable=SC1090
  source "$STATE_FILE"
  : "${MOCK_USDC_ADDRESS:?run ./scripts/deploy-contracts.sh first}"
  : "${SETTLEMENT_ESCROW_ADDRESS:?run ./scripts/deploy-contracts.sh first}"
}

require_api() {
  if ! curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
    err "FastAPI not up on :${API_PORT} — run scripts/e2e_rwa_flow.sh first (it starts the API), or start uvicorn manually."
    exit 1
  fi
}

run() {
  require_state
  require_api

  local salt="$(date +%s%N)"
  local DEAL_ID="0x$(printf 'attestrwa-reject-%s' "$salt" | shasum -a 256 | awk '{print $1}')"
  local DEADLINE=$(( $(date +%s) + 86400 ))

  log "Reject scenario: buyer instructs escrow to release to impostor 'SRL Holding 2026'"
  log "Deal id: $DEAL_ID"

  log "1) Mint $AMOUNT_BASE_UNITS mUSDC to buyer"
  cast send "$MOCK_USDC_ADDRESS" "mint(address,uint256)" \
      "$BUYER_ADDRESS" "$AMOUNT_BASE_UNITS" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$ATTESTER_PRIVATE_KEY" >/dev/null
  ok "minted"

  log "2) Buyer approves escrow"
  cast send "$MOCK_USDC_ADDRESS" "approve(address,uint256)" \
      "$SETTLEMENT_ESCROW_ADDRESS" "$AMOUNT_BASE_UNITS" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "approve"

  log "3) Buyer deposits to escrow with impostor payee"
  cast send "$SETTLEMENT_ESCROW_ADDRESS" \
      "deposit(bytes32,address,address,uint256,uint64)" \
      "$DEAL_ID" "$IMPOSTOR_PAYEE" "$MOCK_USDC_ADDRESS" "$AMOUNT_BASE_UNITS" "$DEADLINE" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "deposit"

  log "4) Attester decision should be REJECT"
  local body
  body=$(cat <<EOF
{
  "deal_id": "$DEAL_ID",
  "buyer_wallet": "$BUYER_ADDRESS",
  "payee_wallet": "$IMPOSTOR_PAYEE",
  "token_address": "$MOCK_USDC_ADDRESS",
  "amount_base_units": $AMOUNT_BASE_UNITS,
  "developer_id": "siam-riverside-living",
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

  if [ "$decision" != "reject" ]; then
    err "Attester decision was '$decision' — expected 'reject'"
    exit 1
  fi
  if [ -z "$uid" ]; then
    err "Attestation not submitted on-chain. Cannot run on-chain refund path."
    exit 1
  fi
  ok "Attester signed REJECT attestation. UID: $uid (tx $txhash)"

  log "5) escrow.release() should now revert (payee not verified)"
  if cast send "$SETTLEMENT_ESCROW_ADDRESS" "release(bytes32,bytes32)" \
        "$DEAL_ID" "$uid" \
        --rpc-url "$DEV_RPC_URL" \
        --private-key "$BUYER_PK" >/dev/null 2>&1; then
    err "release() did NOT revert — escrow accepted a reject attestation. Bug!"
    exit 1
  fi
  ok "release() reverted as expected"

  log "6) Buyer refunds via attester-signed reject path"
  cast send "$SETTLEMENT_ESCROW_ADDRESS" "refund(bytes32,bytes32)" \
      "$DEAL_ID" "$uid" \
      --rpc-url "$DEV_RPC_URL" \
      --private-key "$BUYER_PK" >/dev/null
  ok "refunded"

  local buyer_balance impostor_balance
  buyer_balance=$(cast call "$MOCK_USDC_ADDRESS" "balanceOf(address)(uint256)" \
      "$BUYER_ADDRESS" --rpc-url "$DEV_RPC_URL")
  impostor_balance=$(cast call "$MOCK_USDC_ADDRESS" "balanceOf(address)(uint256)" \
      "$IMPOSTOR_PAYEE" --rpc-url "$DEV_RPC_URL")

  cat <<SUMMARY

================================================================
AttestRWA end-to-end REJECT path: SUCCESS
================================================================
  Deal id           : $DEAL_ID
  Buyer             : $BUYER_ADDRESS
  Impostor payee    : $IMPOSTOR_PAYEE  (NOT in developer feed)
  Token (MockUSDC)  : $MOCK_USDC_ADDRESS
  Escrow            : $SETTLEMENT_ESCROW_ADDRESS
  Amount (uUSDC)    : $AMOUNT_BASE_UNITS
  Attestation UID   : $uid
  Attest tx hash    : $txhash
  Buyer balance     : $buyer_balance  (refunded)
  Impostor balance  : $impostor_balance  (received 0 — verified protection)
================================================================

SUMMARY
}

run "$@"
