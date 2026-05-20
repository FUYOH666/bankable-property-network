#!/usr/bin/env bash
# Start full local AI contour: Qdrant + API + WhatsApp + RAG ingest.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Full Local AI Contour ==="
echo ""
echo "Prerequisites on host Mac:"
echo "  - BGE embedding :9001 + reranker :9002"
echo "  - LM Studio local server :1234/v1"
echo ""

check_host() {
  local name="$1"
  local url="$2"
  if curl -sf "$url" >/dev/null 2>&1; then
    echo "  OK  $name"
    return 0
  fi
  echo "  WARN $name not reachable at $url"
  return 1
}

check_host "BGE embedding" "http://localhost:9001/healthz" || \
  check_host "BGE embedding (livez)" "http://localhost:9001/livez" || true
check_host "BGE reranker" "http://localhost:9002/healthz" || \
  check_host "BGE reranker (livez)" "http://localhost:9002/livez" || true
check_host "LM Studio" "http://localhost:1234/v1/models" || true

echo ""
echo "Starting Docker stack (qdrant + bankable-api + whatsapp-bridge)..."
docker compose -f infra/docker-compose.yml up -d --build qdrant bankable-api whatsapp-bridge

echo "Waiting for API..."
for _ in $(seq 1 30); do
  if curl -sf http://localhost:8080/healthz >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

echo ""
echo "RAG ingest (synthetic + consult KB)..."
curl -sf -X POST "http://localhost:8080/api/rag/ingest" | python3 -m json.tool || \
  echo "Ingest failed — BGE/Qdrant may be down; consult will use keyword fallback."

echo ""
echo "Contour health:"
curl -sf http://localhost:8080/api/consult/contour/healthz | python3 -m json.tool

echo ""
echo "Consult smoke:"
curl -sf -X POST http://localhost:8080/api/consult/message \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"full-contour-smoke","message":"сколько стоит квартира FET","channel":"web"}' \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print('intent:',d.get('intent'),'mode:',d.get('retrieval_mode'))"

echo ""
echo "WhatsApp pairing: http://localhost:8020/pair"
echo "Done."
