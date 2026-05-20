#!/usr/bin/env bash
# Stop the AttestRWA dev chain (anvil background process).

set -euo pipefail

ANVIL_PID_FILE="${DEV_ANVIL_PID_FILE:-/tmp/attestrwa-anvil.pid}"
STATE_FILE="${ATTESTRWA_STATE_FILE:-.dev-chain.state}"

log() { printf '[stop-dev-chain] %s\n' "$*" >&2; }

if [ -f "$ANVIL_PID_FILE" ]; then
  pid=$(cat "$ANVIL_PID_FILE")
  if kill -0 "$pid" 2>/dev/null; then
    log "Killing anvil pid $pid…"
    kill "$pid"
    sleep 1
    kill -9 "$pid" 2>/dev/null || true
  else
    log "No process with pid $pid — already stopped."
  fi
  rm -f "$ANVIL_PID_FILE"
fi

# Fallback: kill anything listening on :8545
if command -v lsof >/dev/null 2>&1; then
  port_pid=$(lsof -ti:8545 || true)
  if [ -n "$port_pid" ]; then
    log "Killing leftover process on :8545 (pid $port_pid)…"
    kill -9 "$port_pid" 2>/dev/null || true
  fi
fi

if [ -f "$STATE_FILE" ]; then
  rm -f "$STATE_FILE"
  log "Removed state file $STATE_FILE."
fi

log "Dev chain stopped."
