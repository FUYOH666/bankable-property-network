# Docker Quickstart — API + WhatsApp + Scenarios

One-command booth stack for hackathon demo (synthetic data only).

## Start

From repo root:

```bash
chmod +x scripts/docker-up.sh scripts/docker-smoke.sh scripts/start-full-ai-contour.sh
./scripts/start-full-ai-contour.sh   # full contour: BGE + LM + Qdrant + ingest + smoke
```

Or API + WhatsApp only:

```bash
./scripts/docker-up.sh
```

Or manually:

```bash
docker compose -f infra/docker-compose.yml up -d --build bankable-api whatsapp-bridge
```

Optional RAG (Qdrant only — embeddings still on host):

```bash
docker compose -f infra/docker-compose.yml up -d qdrant
```

## Services

| Service | Port | Purpose |
|---------|------|---------|
| `bankable-api` | 8080 | FastAPI — scenarios, consult, demo endpoints |
| `whatsapp-bridge` | 8020 | QR pairing, inbound WA → consult API |
| `qdrant` | 6333 | Vector store (optional RAG) |

## Host vs Docker URLs

When `bankable-api` runs **inside Docker**, host services use `host.docker.internal`:

| Service | On Mac host | Inside `bankable-api` container |
|---------|-------------|----------------------------------|
| Qdrant | `http://localhost:6333` | `http://qdrant:6333` |
| BGE embedding | `http://localhost:9001` | `http://host.docker.internal:9001` |
| BGE reranker | `http://localhost:9002` | `http://host.docker.internal:9002` |
| LM Studio | `http://localhost:1234/v1` | `http://host.docker.internal:1234/v1` |

On Linux Docker, `extra_hosts: host.docker.internal:host-gateway` is set in compose.

## WhatsApp pairing (test now)

1. `./scripts/docker-up.sh` or compose up as above.
2. Open **http://localhost:8020/qr** — PNG QR code.
3. Phone: WhatsApp → **Settings → Linked devices → Link a device** → scan.
4. Send test message: *"What is the payee mismatch?"* or *"cash route deposit"*.
5. Status: `curl http://localhost:8020/status`

Full booth runbook: [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md).

## Smoke test

```bash
./scripts/docker-smoke.sh
```

## Scenario simulation (all 8 branches)

**Via Docker API** (no local Python path needed):

```bash
uv run python scripts/run_scenario_matrix.py --api-url http://localhost:8080
```

Report written to `docs/SCENARIO_SIMULATION_REPORT.md`.

**Single scenario curl:**

```bash
curl http://localhost:8080/api/scenarios/cash-red-route/run
curl http://localhost:8080/api/scenarios/prelaunch-off-platform-route/run
```

**RAG fallback** (API must be up; Qdrant optional):

```bash
curl "http://localhost:8080/api/scenarios/usdt-mixed-route/rag-run?mode=fallback"
```

## Logs

```bash
docker compose -f infra/docker-compose.yml logs -f whatsapp-bridge
docker compose -f infra/docker-compose.yml logs -f bankable-api
```

## Stop / tear-down

```bash
docker compose -f infra/docker-compose.yml stop whatsapp-bridge bankable-api
docker volume rm $(docker volume ls -q --filter name=whatsapp_session) 2>/dev/null || true
```

Unlink device in WhatsApp → Linked devices after the event.

## Environment

Bridge env in `infra/docker-compose.yml`:

- `BANKABLE_API_URL=http://bankable-api:8080` (internal Docker network)
- `ALLOWED_CHAT_JID` — optional lock to one chat for booth safety

Local LM Studio + BGE (on host Mac, wired via compose):

```bash
# bankable-api in compose already sets:
LOCAL_AI_EMBEDDING_BASE_URL=http://host.docker.internal:9001
LOCAL_AI_RERANKER_BASE_URL=http://host.docker.internal:9002
LOCAL_AI_LLM_INSTRUCT_BASE_URL=http://host.docker.internal:1234/v1
CONSULT_RETRIEVAL_MODE=auto
QDRANT_URL=http://qdrant:6333
```

Without LM Studio, consult uses **explicit template fallback** (logged). Without BGE/Qdrant, consult falls back to **keyword chunk search**.
