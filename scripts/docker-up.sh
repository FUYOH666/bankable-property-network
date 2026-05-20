#!/usr/bin/env bash
# Start API + WhatsApp bridge (hackathon booth stack).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Building and starting bankable-api + whatsapp-bridge..."
docker compose -f infra/docker-compose.yml up -d --build bankable-api whatsapp-bridge

echo ""
echo "Wait for health (up to 90s)..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:8080/healthz >/dev/null 2>&1; then
    echo "  bankable-api OK"
    break
  fi
  sleep 3
done

for i in $(seq 1 30); do
  if curl -sf http://localhost:8020/healthz >/dev/null 2>&1; then
    echo "  whatsapp-bridge OK"
    break
  fi
  sleep 3
done

echo ""
echo "=== Ready ==="
echo "  API health:     curl http://localhost:8080/healthz"
echo "  Consult:        curl http://localhost:8080/api/consult/healthz"
echo "  WA status:      curl http://localhost:8020/status"
echo "  WA QR (scan):   open http://localhost:8020/pair"
echo ""
echo "  Smoke all:      ./scripts/docker-smoke.sh"
echo "  Scenario batch: uv run python scripts/run_scenario_matrix.py --api-url http://localhost:8080"
