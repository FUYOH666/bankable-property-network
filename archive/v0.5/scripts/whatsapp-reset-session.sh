#!/usr/bin/env bash
# Wipe WhatsApp session volume and restart bridge (fixes "failed to link device").
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "Stopping whatsapp-bridge..."
docker compose -f infra/docker-compose.yml stop whatsapp-bridge
docker compose -f infra/docker-compose.yml rm -f whatsapp-bridge

VOLUME="$(docker volume ls -q --filter name=whatsapp_session | head -1)"
if [[ -n "${VOLUME}" ]]; then
  echo "Removing volume ${VOLUME}..."
  docker volume rm "${VOLUME}"
else
  echo "No whatsapp_session volume found (already clean)."
fi

echo "Rebuilding and starting whatsapp-bridge..."
docker compose -f infra/docker-compose.yml up -d --build whatsapp-bridge

echo ""
echo "Wait ~10s, then open: http://localhost:8020/pair"
echo "Scan QR within 20 seconds of page load."
echo "Status: curl -s http://localhost:8020/status | python3 -m json.tool"
