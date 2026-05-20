# Deploy — Bankable Property OS API

This repo deploys as **two artifacts**:

1. **FastAPI API** — live demo backend (required for Closing Passport hash, scenarios, RAG).
2. **Next.js web** (`apps/web`) — optional standalone demo UI, or embed via website-scanovich.ai.

## API — Docker

Build from repository root:

```bash
docker build -t bankable-property-os-api .
docker run -p 8080:8080 \
  -e BANKABLE_CORS_ORIGINS=https://scanovich.ai,http://localhost:3000 \
  bankable-property-os-api
```

Smoke:

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/api/demo/closing-passport
curl http://localhost:8080/api/demo/developer-knowledge-hub
curl http://localhost:8080/api/demo/guided-simulation
curl http://localhost:8080/api/demo/evidence-pack
curl http://localhost:8080/api/demo/post-closing-yield-plan
curl http://localhost:8080/api/scenarios
```

## API — Render (render.yaml)

Use the included `render.yaml` as a starting point. Set environment variables in Render dashboard:

| Variable | Example |
|----------|---------|
| `BANKABLE_CORS_ORIGINS` | `https://scanovich.ai,https://www.scanovich.ai` |
| `QDRANT_URL` | Your Qdrant instance (optional for RAG) |
| `LOCAL_AI_EMBEDDING_BASE_URL` | Embedding service URL (optional) |
| `LOCAL_AI_RERANKER_BASE_URL` | Reranker service URL (optional) |

**Note:** Render deploy covers the FastAPI API only — not the full local AI stack (Qdrant, BGE, LM Studio). Production AI inference is separate infrastructure; see [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

Health check path: `/healthz`

## Web — Standalone

```bash
cd apps/web
NEXT_PUBLIC_SEABW_API_URL=https://your-api.example.com pnpm build
pnpm start
```

For static export to a CDN, configure `output: 'export'` in Next config if needed. Default app uses client-side fetch and requires a live API for full demo.

## Environment

Copy `.env.example` to `.env` for local development. Never commit `.env`.

## Security

- Do not commit real TailScale IPs, API keys, or internal hostnames.
- Use placeholder URLs in public docs.
- Verify `BANKABLE_CORS_ORIGINS` before production deploy.

## Related

- Website integration: `docs/PUBLISH_SEABLOCKCHAINWEEK.md`
- Demo runbook: `docs/HACKATHON_RUNBOOK.md`
- Local AI contour: `docs/LOCAL_AI_CONTOUR.md`
- AI service tiers: `docs/AI_SERVICE_TIERS.md`
