#!/usr/bin/env bash
# Smoke test Docker stack: API, consult, scenarios, WhatsApp bridge.
set -euo pipefail

API="${BANKABLE_API_URL:-http://localhost:8080}"
WA="${WHATSAPP_BRIDGE_URL:-http://localhost:8020}"

echo "=== bankable-api ==="
curl -sf "$API/healthz" | head -c 200
echo ""
curl -sf "$API/api/consult/healthz" | head -c 300
echo ""

echo "=== scenario run (swift-clean) ==="
curl -sf "$API/api/scenarios/swift-clean-route/run" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('bank_action:', d.get('bank_action'), '| passport:', d.get('closing_passport_status'))
"

echo "=== consult contour ==="
curl -sf "$API/api/consult/contour/healthz" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('all_ready:', d.get('all_ready'), '| mode:', d.get('consult_retrieval_mode'))
llm=d.get('services',{}).get('llm_instruct',{})
print('llm_configured:', llm.get('ready'), '-', llm.get('detail'))
"

echo "=== consult message ==="
curl -sf -X POST "$API/api/consult/message" \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"docker-smoke","message":"payee mismatch on anchor case","channel":"web"}' \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('mode:', d.get('retrieval_mode'))
print('reply:', (d.get('reply') or '')[:200], '...')
"

echo "=== whatsapp-bridge ==="
curl -sf "$WA/healthz" | head -c 200
echo ""
curl -sf "$WA/status" | python3 -m json.tool

echo ""
echo "QR pairing: open $WA/qr in browser, scan with WhatsApp → Linked devices"
echo "All smoke checks passed."
