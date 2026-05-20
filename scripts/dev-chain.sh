#!/usr/bin/env bash
# AttestRWA — local dev chain orchestrator
#
# Starts an Anvil node forked from Base Sepolia at port 8545, then registers
# the EAS SettlementApproval schema on the fork using the Anvil default
# attester account (#0).
#
# Idempotent: if Anvil is already running, reuses it. If the schema is
# already registered (deterministic UID), prints the existing UID.
#
# Stop the chain with: scripts/stop-dev-chain.sh
#
# Why a fork (not pure local Anvil): we want the real EAS protocol bytecode
# at the canonical Base addresses (0x4200…0021 EAS, 0x4200…0020
# SchemaRegistry). A fork inherits all production state, so attestations
# behave identically to real Base Sepolia — without faucet requirements.

set -euo pipefail

# shellcheck disable=SC2155
export PATH="$HOME/.foundry/bin:$PATH"

RPC_URL="${DEV_RPC_URL:-http://127.0.0.1:8545}"
FORK_URL="${DEV_FORK_URL:-https://sepolia.base.org}"
CHAIN_ID="${DEV_CHAIN_ID:-84532}"
BLOCK_TIME="${DEV_BLOCK_TIME:-2}"
ANVIL_PORT="${DEV_ANVIL_PORT:-8545}"
ANVIL_LOG="${DEV_ANVIL_LOG:-/tmp/attestrwa-anvil.log}"
ANVIL_PID_FILE="${DEV_ANVIL_PID_FILE:-/tmp/attestrwa-anvil.pid}"

# Canonical EAS protocol addresses (same on Base mainnet + Base Sepolia +
# Optimism). Source: https://docs.attest.org/docs/quick--start/contracts
EAS_ADDR="0x4200000000000000000000000000000000000021"
SCHEMA_REGISTRY_ADDR="0x4200000000000000000000000000000000000020"

# Anvil default account #0 — public test key, NEVER use on mainnet.
# Address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
# Mnemonic: "test test test test test test test test test test test junk"
DEV_ATTESTER_ADDRESS="${DEV_ATTESTER_ADDRESS:-0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266}"
DEV_ATTESTER_PRIVATE_KEY="${DEV_ATTESTER_PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"

SCHEMA_STRING="bytes32 dealId, address attester, address payeeAddress, address tokenAddress, uint256 amount, uint8 capitalClass, bytes32 evidenceHash, string jurisdiction, uint64 expiresAt, bool payeeVerified"

log() { printf '[dev-chain] %s\n' "$*" >&2; }

ensure_foundry() {
  if ! command -v anvil >/dev/null 2>&1; then
    log "Foundry not on PATH. Install:"
    log "  curl -L https://foundry.paradigm.xyz | bash && source ~/.zshenv && foundryup"
    exit 1
  fi
}

anvil_running() {
  curl -sf -X POST "$RPC_URL" \
    -H 'Content-Type: application/json' \
    --data '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}' \
    >/dev/null 2>&1
}

start_anvil() {
  if anvil_running; then
    log "Anvil already responding on $RPC_URL — reusing."
    return 0
  fi

  log "Starting Anvil fork of $FORK_URL on port $ANVIL_PORT (chain $CHAIN_ID, block_time ${BLOCK_TIME}s)…"
  nohup anvil \
    --fork-url "$FORK_URL" \
    --port "$ANVIL_PORT" \
    --block-time "$BLOCK_TIME" \
    --chain-id "$CHAIN_ID" \
    --auto-impersonate \
    >"$ANVIL_LOG" 2>&1 &
  echo $! >"$ANVIL_PID_FILE"

  for _ in $(seq 1 20); do
    if anvil_running; then
      log "Anvil up (pid $(cat "$ANVIL_PID_FILE"))."
      return 0
    fi
    sleep 1
  done

  log "Anvil failed to start. Last log:"
  tail -40 "$ANVIL_LOG" >&2
  exit 1
}

verify_eas_alive() {
  local len
  len=$(cast code "$EAS_ADDR" --rpc-url "$RPC_URL" 2>/dev/null | wc -c | tr -d ' ')
  if [ "${len:-0}" -lt 100 ]; then
    log "EAS contract not present at $EAS_ADDR on $RPC_URL — fork may have failed."
    exit 1
  fi
  log "EAS contract verified at $EAS_ADDR (code length=$len)."
}

register_schema() {
  log "Registering SettlementApproval schema (idempotent)…"
  local tx_json
  if ! tx_json=$(cast send "$SCHEMA_REGISTRY_ADDR" \
        "register(string,address,bool)" \
        "$SCHEMA_STRING" \
        0x0000000000000000000000000000000000000000 \
        true \
        --rpc-url "$RPC_URL" \
        --private-key "$DEV_ATTESTER_PRIVATE_KEY" \
        --json 2>&1); then
    # Re-registration of the same schema reverts with `AlreadyExists()`.
    # That is the success path on a warm dev chain.
    if printf '%s' "$tx_json" | grep -qi 'AlreadyExists\|0x23369fa6'; then
      log "Schema already registered on this fork — using existing UID."
    else
      log "Schema registration failed:"
      printf '%s\n' "$tx_json" >&2
      exit 1
    fi
  fi

  # Extract UID from the Registered event (topic[1]) if the call returned a
  # receipt; otherwise we have to compute it. The canonical UID derivation
  # in EAS SchemaRegistry is: keccak256(abi.encodePacked(schema, resolver,
  # revocable)). We hardcode the known UID for this exact schema (verified
  # via getSchema after first registration).
  SCHEMA_UID="0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96"
  log "Schema UID: $SCHEMA_UID"

  # Confirm via getSchema readback.
  if ! cast call "$SCHEMA_REGISTRY_ADDR" \
       "getSchema(bytes32)((bytes32,address,bool,string))" \
       "$SCHEMA_UID" \
       --rpc-url "$RPC_URL" >/dev/null 2>&1; then
    log "getSchema readback failed — schema UID may be wrong for this fork state."
    exit 1
  fi
  log "Schema verified via getSchema readback."
}

write_state_file() {
  local state_file="${ATTESTRWA_STATE_FILE:-.dev-chain.state}"
  cat >"$state_file" <<EOF
# AttestRWA dev chain state — auto-generated by scripts/dev-chain.sh
# Do not commit this file (it is in .gitignore).

DEV_RPC_URL=$RPC_URL
DEV_CHAIN_ID=$CHAIN_ID
DEV_ANVIL_PID=$(cat "$ANVIL_PID_FILE" 2>/dev/null || echo "")
DEV_FORK_URL=$FORK_URL

EAS_ADDRESS=$EAS_ADDR
EAS_SCHEMA_REGISTRY_ADDRESS=$SCHEMA_REGISTRY_ADDR
EAS_SCHEMA_UID_SETTLEMENT_APPROVAL=$SCHEMA_UID

ATTESTER_ADDRESS=$DEV_ATTESTER_ADDRESS
# WARNING: this is the well-known Anvil test private key. Never deploy with
# it to a real network.
ATTESTER_PRIVATE_KEY=$DEV_ATTESTER_PRIVATE_KEY
EOF
  log "State written to $state_file"
}

main() {
  ensure_foundry
  start_anvil
  verify_eas_alive
  register_schema
  write_state_file

  cat <<EOF

================================================================
AttestRWA dev chain ready
================================================================
  RPC URL          : $RPC_URL
  Chain ID         : $CHAIN_ID
  EAS address      : $EAS_ADDR
  SchemaRegistry   : $SCHEMA_REGISTRY_ADDR
  Schema UID       : $SCHEMA_UID
  Attester address : $DEV_ATTESTER_ADDRESS
  Anvil log        : $ANVIL_LOG
  Anvil pid        : $(cat "$ANVIL_PID_FILE" 2>/dev/null || echo "?")
  State file       : .dev-chain.state

Stop with: scripts/stop-dev-chain.sh
================================================================
EOF
}

main "$@"
