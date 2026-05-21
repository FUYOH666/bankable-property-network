# WhatsApp bridge (hackathon demo)

Personal-account WhatsApp bridge for the Buyer Consultation API. **Synthetic demo only.**

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz` | Liveness |
| GET | `/status` | `paired` / `waiting_for_qr_scan` / `connecting` |
| GET | `/qr` | PNG QR code while unpaired |
| GET | `/qr?format=json` | Base64 PNG in JSON |

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `BANKABLE_API_URL` | `http://localhost:8080` | FastAPI consult endpoint base |
| `WHATSAPP_SESSION_PATH` | `/data/session/whatsapp.db` | SQLite session store |
| `WHATSAPP_BRIDGE_ADDR` | `:8020` | HTTP listen address |
| `ALLOWED_CHAT_JID` | *(empty)* | Optional lock to one chat JID |

## Local run

```bash
cd services/whatsapp-bridge
go mod tidy
go run .
```

With Docker Compose (from repo root):

```bash
docker compose -f infra/docker-compose.yml up -d bankable-api whatsapp-bridge
open http://localhost:8020/qr
```

See [`docs/WHATSAPP_CONSULT_DEMO.md`](../../docs/WHATSAPP_CONSULT_DEMO.md) for booth setup and tear-down.
