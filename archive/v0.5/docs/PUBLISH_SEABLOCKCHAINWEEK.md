# Publish — SEA Blockchain Week on scanovich.ai

Handoff for publishing the hackathon demo at **`https://scanovich.ai/seablockchainweek/`**.

## Architecture

```text
scanovich.ai (website-scanovich.ai repo, static export)
  └── /seablockchainweek/          ← landing + demo UI (fetch to API)

<separate deploy from this repo>
  └── FastAPI (Bankable Property OS API)
      GET /healthz
      GET /api/demo/*
      GET /api/scenarios/*
```

Pushing to the website repo **does not** start FastAPI. Deploy API separately first.

## Step 1 — Deploy API

Follow `docs/DEPLOY.md`. Example public URL (replace with yours):

```text
https://seabw-api.example.com
```

Verify:

```bash
curl https://seabw-api.example.com/healthz
curl https://seabw-api.example.com/api/demo/closing-passport
curl https://seabw-api.example.com/api/demo/developer-knowledge-hub
curl https://seabw-api.example.com/api/demo/supplier-contrast
curl https://seabw-api.example.com/api/demo/guided-simulation
curl https://seabw-api.example.com/api/demo/evidence-pack
curl https://seabw-api.example.com/api/demo/post-closing-yield-plan
```

Ensure CORS includes scanovich.ai:

```bash
BANKABLE_CORS_ORIGINS=https://scanovich.ai,https://www.scanovich.ai
```

## Step 2 — Website Page (website-scanovich.ai repo)

Create route: `app/seablockchainweek/page.tsx`

Recommended constants:

```typescript
export const SEABLOCKCHAINWEEK_PATH = '/seablockchainweek/';
```

Build-time env on Render (or CI):

```bash
NEXT_PUBLIC_SEABW_API_URL=https://seabw-api.example.com
```

UI options:

| Option | Description |
|--------|-------------|
| A (recommended) | Landing on scanovich.ai with iframe or link to deployed `apps/web` subdomain |
| B | Embed key demo components from this repo |
| C | Full copy of demo page into website repo |

Navigation: no main nav item. Optional `noindex`, exclude from sitemap.

## Step 3 — Smoke After Publish

- [ ] `https://scanovich.ai/seablockchainweek/` loads
- [ ] Browser fetch to API succeeds (no CORS error)
- [ ] Developer Knowledge Hub shows payee mismatch
- [ ] Supplier Contrast panel loads (Shadow Bay vs Bangkok Landmark)
- [ ] Settlement Flow panel shows evidence hash and route comparison
- [ ] Scenario simulator lists 8 scenarios
- [ ] Post-Closing Yield Plan loads
- [ ] Guided Simulation Evidence Pack JSON link works

## Judges Handoff

Provide two URLs:

```text
Demo UI:  https://scanovich.ai/seablockchainweek/
API:      https://seabw-api.example.com/healthz
Pitch:    docs/PITCH_SCRIPT.md (3-minute money infrastructure flow)
Thesis:   docs/MONEY_INFRASTRUCTURE_THESIS.md
Audit:    docs/AI_AUDIT_INDEX.md (live vs roadmap, invariants)
Register: docs/PROJECT_DESCRIPTION.md (hackathon form copy)
```

## Local Development

```bash
# Terminal 1 — API
cd apps/api && uv run uvicorn app.main:app --app-dir src --port 8080

# Terminal 2 — Web
cd apps/web && pnpm dev
```

Web uses `NEXT_PUBLIC_SEABW_API_URL` or `NEXT_PUBLIC_BANKABLE_API_URL` (see `apps/web/src/lib/api-base-url.ts`).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| CORS error in browser | Add scanovich.ai to `BANKABLE_CORS_ORIGINS`, redeploy API |
| Empty Closing Passport | API not running or wrong `NEXT_PUBLIC_SEABW_API_URL` at build time |
| Settlement Flow empty | Same as above — panel uses `/api/demo/closing-passport` |
| RAG unavailable | Expected without Qdrant/BGE; deterministic fallback still works |

## Do Not Publish

- `.env` files with real secrets
- TailScale or internal IP addresses in public README
- Claims of legal title guarantee or regulator approval
