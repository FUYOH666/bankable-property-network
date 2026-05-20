#!/usr/bin/env bash
# AttestRWA — boot the entire demo stack with one command.
#
# Composes:
#   1. ./scripts/dev-chain.sh        — Anvil fork of Base Sepolia + EAS schema registered
#   2. ./scripts/deploy-contracts.sh — MockUSDC + SettlementEscrow deployed
#   3. uvicorn backend (FastAPI attester) on :8080
#   4. Next.js web dev server on :3000
#
# Idempotent across restarts: each step exits early if its child process is
# already healthy. Shutdown via ./scripts/stop-demo-mode.sh.
#
# Recording-friendly: every milestone prints in bold green so the demo is
# easy to follow on screen.

set -euo pipefail

# shellcheck disable=SC2155
export PATH="$HOME/.foundry/bin:$PATH"

API_HOST=127.0.0.1
API_PORT=${ATTESTRWA_API_PORT:-8080}
WEB_PORT=${ATTESTRWA_WEB_PORT:-3000}
API_LOG=/tmp/attestrwa-api.log
WEB_LOG=/tmp/attestrwa-web.log
API_PID_FILE=/tmp/attestrwa-api.pid
WEB_PID_FILE=/tmp/attestrwa-web.pid

green()  { printf '\033[1;32m%s\033[0m\n' "$*"; }
cyan()   { printf '\033[1;36m%s\033[0m\n' "$*"; }
yellow() { printf '\033[1;33m%s\033[0m\n' "$*"; }
red()    { printf '\033[1;31m%s\033[0m\n' "$*"; }

step() {
  printf '\n'
  cyan "================================================================"
  cyan "$1"
  cyan "================================================================"
}

is_listening() {
  local port=$1
  curl -fsS "http://${API_HOST}:${port}/" >/dev/null 2>&1 \
    || curl -fsS "http://${API_HOST}:${port}/healthz" >/dev/null 2>&1
}

# ---- 1. Dev chain ------------------------------------------------------

step "1) Dev chain — Anvil fork of Base Sepolia (canonical EAS at 0x4200…0021)"
./scripts/dev-chain.sh

# ---- 2. Contracts ------------------------------------------------------

step "2) Contracts — deploy MockUSDC + SettlementEscrow"
if ! grep -q '^SETTLEMENT_ESCROW_ADDRESS=0x' .dev-chain.state 2>/dev/null; then
  ./scripts/deploy-contracts.sh
else
  green "Contracts already deployed (per .dev-chain.state) — reusing."
fi

# Re-source after the deploy script appends addresses
# shellcheck disable=SC1091
source .dev-chain.state

# ---- 3. Attester service ----------------------------------------------

step "3) FastAPI attester on :${API_PORT}"
if curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
  green "FastAPI already healthy — reusing."
else
  rm -f "$API_PID_FILE"
  (
    cd apps/api
    DEV_RPC_URL="$DEV_RPC_URL" \
    EAS_SCHEMA_UID_SETTLEMENT_APPROVAL="$EAS_SCHEMA_UID_SETTLEMENT_APPROVAL" \
    ATTESTER_ADDRESS="$ATTESTER_ADDRESS" \
    ATTESTER_PRIVATE_KEY="$ATTESTER_PRIVATE_KEY" \
    EAS_ADDRESS="$EAS_ADDRESS" \
    DEV_CHAIN_ID="$DEV_CHAIN_ID" \
    nohup uv run uvicorn app.main:app --app-dir src --host "$API_HOST" --port "$API_PORT" \
      >"$API_LOG" 2>&1 &
    echo $! > "$API_PID_FILE"
  )
  for _ in $(seq 1 30); do
    if curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
      green "FastAPI healthy (pid $(cat "$API_PID_FILE"))."
      break
    fi
    sleep 1
  done
  if ! curl -fsS "http://${API_HOST}:${API_PORT}/healthz" >/dev/null 2>&1; then
    red "FastAPI did not come up. Last 20 lines of $API_LOG:"
    tail -20 "$API_LOG"
    exit 1
  fi
fi

# ---- 4. Next.js web dev ------------------------------------------------

step "4) Next.js web on :${WEB_PORT}"
if is_listening "$WEB_PORT"; then
  green "Web dev server already responding — reusing."
else
  rm -f "$WEB_PID_FILE"
  (
    cd apps/web
    NEXT_PUBLIC_API_BASE_URL="http://${API_HOST}:${API_PORT}" \
    NEXT_PUBLIC_RPC_URL="$DEV_RPC_URL" \
    NEXT_PUBLIC_CHAIN_ID="$DEV_CHAIN_ID" \
    NEXT_PUBLIC_ESCROW_ADDRESS="$SETTLEMENT_ESCROW_ADDRESS" \
    NEXT_PUBLIC_MOCK_USDC_ADDRESS="$MOCK_USDC_ADDRESS" \
    NEXT_PUBLIC_ATTESTER_ADDRESS="$ATTESTER_ADDRESS" \
    NEXT_PUBLIC_EAS_SCHEMA_UID="$EAS_SCHEMA_UID_SETTLEMENT_APPROVAL" \
    NEXT_PUBLIC_BASESCAN_URL="https://sepolia.basescan.org" \
    NEXT_PUBLIC_EAS_SCAN_URL="https://base-sepolia.easscan.org" \
    nohup pnpm dev --port "$WEB_PORT" \
      >"$WEB_LOG" 2>&1 &
    echo $! > "$WEB_PID_FILE"
  )
  for _ in $(seq 1 60); do
    if is_listening "$WEB_PORT"; then
      green "Web up (pid $(cat "$WEB_PID_FILE"))."
      break
    fi
    sleep 1
  done
  if ! is_listening "$WEB_PORT"; then
    red "Next.js dev did not come up. Last 20 lines of $WEB_LOG:"
    tail -20 "$WEB_LOG"
    exit 1
  fi
fi

# ---- Summary -----------------------------------------------------------

step "DEMO READY"

cat <<EOF

  $(green "AttestRWA stack is live.")

  $(yellow "On-chain (local Anvil fork of Base Sepolia)")
    RPC URL              : $DEV_RPC_URL
    Chain ID             : $DEV_CHAIN_ID
    EAS contract         : $EAS_ADDRESS
    Schema UID           : $EAS_SCHEMA_UID_SETTLEMENT_APPROVAL
    SettlementEscrow     : $SETTLEMENT_ESCROW_ADDRESS
    MockUSDC             : $MOCK_USDC_ADDRESS
    Attester EOA         : $ATTESTER_ADDRESS

  $(yellow "Backend (FastAPI attester)")
    Health               : http://${API_HOST}:${API_PORT}/healthz
    Attest endpoint      : http://${API_HOST}:${API_PORT}/attest/settlement
    Attester healthz     : http://${API_HOST}:${API_PORT}/attest/healthz
    Farcaster Frame      : http://${API_HOST}:${API_PORT}/api/frame/attest?decision=approve
    Logs                 : $API_LOG

  $(yellow "Web (Next.js)")
    Hero                 : http://${API_HOST}:${WEB_PORT}/
    Live demo screen     : http://${API_HOST}:${WEB_PORT}/rwa-settlement-live
    Logs                 : $WEB_LOG

  $(yellow "Recording-ready commands")
    Happy path E2E       : ./scripts/e2e_rwa_flow.sh
    Reject path E2E      : ./scripts/e2e_rwa_reject.sh
    Full recording guide : docs/HACKATHON_RECORDING_GUIDE.md

  $(yellow "Stop everything")
    ./scripts/stop-demo-mode.sh

EOF
