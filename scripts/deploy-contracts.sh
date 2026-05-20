#!/usr/bin/env bash
# Deploy SettlementEscrow + MockUSDC against the local dev chain. Reads the
# attester key and schema UID from .dev-chain.state (produced by
# scripts/dev-chain.sh).
#
# Idempotent across full restarts of the dev chain — anvil starts at a
# known fork height with deterministic nonces, so the resulting addresses
# are stable as long as the deployer EOA + nonce sequence are the same.
#
# Outputs deployed addresses both as console block and as ENV-like exports
# appended to .dev-chain.state (so apps can `source .dev-chain.state` to
# pick up MOCK_USDC_ADDRESS / SETTLEMENT_ESCROW_ADDRESS).

set -euo pipefail

# shellcheck disable=SC2155
export PATH="$HOME/.foundry/bin:$PATH"

STATE_FILE="${ATTESTRWA_STATE_FILE:-.dev-chain.state}"

if [ ! -f "$STATE_FILE" ]; then
  echo "[deploy] $STATE_FILE not found. Run ./scripts/dev-chain.sh first." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$STATE_FILE"

log() { printf '[deploy] %s\n' "$*" >&2; }

cd contracts

log "Building contracts…"
forge build --silent

log "Deploying MockUSDC + SettlementEscrow to $DEV_RPC_URL …"

OUTPUT=$(PRIVATE_KEY="$ATTESTER_PRIVATE_KEY" \
  EAS_SCHEMA_UID_SETTLEMENT_APPROVAL="$EAS_SCHEMA_UID_SETTLEMENT_APPROVAL" \
  ATTESTER_ADDRESS="$ATTESTER_ADDRESS" \
  forge script script/Deploy.s.sol \
  --rpc-url "$DEV_RPC_URL" \
  --broadcast \
  --skip-simulation 2>&1)

MOCK_USDC_ADDRESS=$(echo "$OUTPUT" | awk '/MockUSDC[[:space:]]*:/ {print $NF}')
SETTLEMENT_ESCROW_ADDRESS=$(echo "$OUTPUT" | awk '/SettlementEscrow:/ {print $NF}')

if [ -z "$MOCK_USDC_ADDRESS" ] || [ -z "$SETTLEMENT_ESCROW_ADDRESS" ]; then
  echo "[deploy] Could not parse deploy addresses from script output:" >&2
  echo "$OUTPUT" >&2
  exit 1
fi

# Persist for downstream services
{
  echo ""
  echo "# Contract addresses (appended by scripts/deploy-contracts.sh)"
  echo "MOCK_USDC_ADDRESS=$MOCK_USDC_ADDRESS"
  echo "SETTLEMENT_ESCROW_ADDRESS=$SETTLEMENT_ESCROW_ADDRESS"
} >> "../$STATE_FILE"

cat <<EOF

================================================================
AttestRWA contracts deployed
================================================================
  MockUSDC            : $MOCK_USDC_ADDRESS
  SettlementEscrow    : $SETTLEMENT_ESCROW_ADDRESS
  Trusted attester    : $ATTESTER_ADDRESS
  Schema UID          : $EAS_SCHEMA_UID_SETTLEMENT_APPROVAL
  RPC                 : $DEV_RPC_URL
  Deployer pre-minted : 1,000,000 mUSDC

Addresses appended to ../$STATE_FILE
================================================================
EOF
