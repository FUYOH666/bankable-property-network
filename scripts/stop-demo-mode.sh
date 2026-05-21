#!/usr/bin/env bash
# AttestRWA — stop everything started by ./scripts/demo-mode.sh.

set -euo pipefail

API_PID_FILE=/tmp/attestrwa-api.pid
WEB_PID_FILE=/tmp/attestrwa-web.pid

log() { printf '[stop-demo] %s\n' "$*" >&2; }

kill_pid_file() {
  local file=$1 label=$2
  if [ -f "$file" ]; then
    local pid
    pid=$(cat "$file")
    if kill -0 "$pid" 2>/dev/null; then
      log "Killing $label (pid $pid)…"
      kill "$pid" 2>/dev/null || true
      sleep 1
      kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$file"
  fi
}

kill_pid_file "$WEB_PID_FILE" "Next.js web"
kill_pid_file "$API_PID_FILE" "FastAPI attester"

# Belt-and-suspenders: free the ports
for port in 3000 8080; do
  if command -v lsof >/dev/null 2>&1; then
    leftover=$(lsof -ti:$port 2>/dev/null || true)
    if [ -n "$leftover" ]; then
      log "Killing leftover on :$port (pid $leftover)…"
      kill -9 "$leftover" 2>/dev/null || true
    fi
  fi
done

./scripts/stop-dev-chain.sh

log "Demo stack stopped."
