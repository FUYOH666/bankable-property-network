# Reproduction Guide — Bankable Property Network

**Purpose:** rebuild this hackathon MVP from zero, or onboard a parallel team while another track continues the existing repo.

**Current reference version:** 0.5.5 · **Last aligned:** 2026-05-20

**Companion docs:** thesis [`MONEY_INFRASTRUCTURE_THESIS.md`](MONEY_INFRASTRUCTURE_THESIS.md) · live status [`HANDOFF.md`](HANDOFF.md) · agent entry [`../AGENTS.md`](../AGENTS.md) · AI audit [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md)

---

## 0. What you are building (one paragraph)

**Bankable Property Network** is bank-grade money infrastructure for Thailand property. Primary customer: **banking anchor / regulated structures**. Buyer protection is a **social bonus**.

Product stack:

```text
Developer Knowledge (SSOT) → Property Shield → Capital Map → Route Comparison
  → Bank Counter-Offer → Compliance gate → Closing Passport → Yield OS (vision)
```

Anchor story: foreign buyer, 12M THB Bangkok condo, Dubai bank + USDT, agent sends deposit to **wrong legal entity** (`SRL Holding 2026` vs developer `Siam Riverside Living Co., Ltd.`).

---

## 1. Two tracks — choose yours

| Track | When | Action |
|-------|------|--------|
| **Continue existing repo** | You already have this codebase | Read [`HANDOFF.md`](HANDOFF.md), run smoke, extend modules below |
| **Rebuild from scratch** | New hackathon team, clean room | Follow Phases 2–8 in order; copy synthetic data shapes from this repo |
| **Fork & customize** | Same thesis, different bank/region | Keep architecture; replace `data/synthetic/` and anchor case |

---

## 2. Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.12+ | API only via **uv** (no global pip) |
| uv | latest | `uv sync`, `uv run pytest` |
| Node.js | 20+ | for Next.js |
| pnpm | 9+ | lockfile required |
| Docker | optional | Qdrant for live RAG |
| Git | — | `.env` never committed |

```bash
cp .env.example .env   # placeholders only
```

---

## 3. Target repository layout

```text
SCB-money-care-OS/
├── AGENTS.md                 # agent entry (short)
├── apps/
│   ├── api/                  # FastAPI — rules, demo endpoints, RAG
│   │   src/app/
│   │   │   main.py
│   │   │   demo_case.py      # ANCHOR_CASE constant
│   │   │   paths.py          # repo root resolution
│   │   │   config.py         # pydantic-settings
│   │   │   services/         # engines (see Phase 4)
│   │   │   schemas/          # Pydantic response models
│   │   └── tests/
│   └── web/                  # Next.js demo UI
│       src/app/              # page + vision screens
│       src/lib/              # use-demo-fetch, api-base-url
├── data/synthetic/           # SSOT for demo + RAG corpus
├── docs/                     # thesis, runbooks, this file
├── infra/docker-compose.yml  # Qdrant
├── Dockerfile                # API deploy
└── CHANGELOG.md
```

---

## 4. Build phases (recommended order)

### Phase A — Scaffold (2–4 h)

1. Monorepo folders: `apps/api`, `apps/web`, `data/synthetic`, `docs`, `infra`.
2. FastAPI app with `GET /healthz` → `{ "status": "ok" }`.
3. Next.js app with hero + static pitch paragraph.
4. `uv sync` + `pnpm install`; CI = pytest + build.

**Gate:** `curl localhost:8080/healthz` and `pnpm dev` loads page.

---

### Phase B — Anchor case + synthetic corpus (3–5 h)

**Goal:** one deterministic story every engine consumes.

1. Create [`demo_case.py`](../apps/api/src/app/demo_case.py) — `ANCHOR_CASE` with:
   - `expected_payee` vs `payment_instruction_payee` (mismatch)
   - `capital_sources`: bank (green), USDT (amber), P2P (red)
   - `deposit_deadline_hours` for urgency flag

2. Populate `data/synthetic/` minimum set:

   | Path | Role |
   |------|------|
   | `policies/property_settlement_policy.md` | RAG + compliance narrative |
   | `policies/commission_model_and_entry_barrier.md` | Thesis backing |
   | `developers/siam-riverside-feed.json` | Developer Knowledge SSOT |
   | `scenarios/scenarios.json` + projects/agents/buyers/banks | Scenario simulator |
   | `cases/anchor-deposit-mismatch/*` | Case documents |

3. Add `paths.py` + `data_loader.load_json()` — single way to read synthetic JSON.

**Gate:** `load_json("developers/siam-riverside-feed.json")` works from API cwd.

**Expand quality:**
- Add more developers/projects; multi-feed ingestion stub.
- JSON Schema validation on load.
- Freshness timestamps + SLA policy in feed.

---

### Phase C — Core settlement engines (4–6 h)

Build pure functions first (unit tests, no HTTP):

| Module | File | Input → Output |
|--------|------|----------------|
| Property Shield | `services/risk_engine.py` | case → `{ risk_level, flags[] }` |
| Capital Map | `services/capital.py` | sources[] → `{ id: { status, reason } }` |
| Route Comparison | `services/routing.py` | risk + capital → routes[]; **always** one `bankable_escrow` recommended |
| Evidence Pack | `services/evidence_pack.py` | case + risk + capital + route → hash + attestation (no PII) |

Helper: `pick_recommended_route(routes)` — never bare `next(...)` without fallback.

Orchestrator: `services/closing_passport_demo.py` — memoized builder for anchor case.

**Endpoint:** `GET /api/demo/closing-passport`

**Gate:** pytest for mismatch flag, capital colors, escrow recommended, deterministic hash.

**Expand quality:**
- Configurable rules YAML instead of hardcoded flags.
- Payee fuzzy match (normalize Ltd./Co.).
- Multi-route scoring with explainability JSON.
- PDF export of evidence pack.

---

### Phase D — Developer Knowledge Layer (2–3 h)

**Goal:** upstream SSOT before Property Shield.

1. `services/developer_knowledge.py` — load feed, compare `case.payment_instruction_payee` vs `authorized_payees`.
2. `GET /api/demo/developer-knowledge-hub`
3. UI: `developer-knowledge-hub.tsx` via `useDemoFetch`.

**Gate:** `knowledge_vs_agent_gap.status == "mismatch_detected"` on anchor.

**Expand quality:**
- Real ERP webhook ingestion (CSV/API).
- Multi-developer feeds; tenant isolation.
- Channel roadmap: WhatsApp/Telegram (see [`DEVELOPER_KNOWLEDGE_LAYER.md`](DEVELOPER_KNOWLEDGE_LAYER.md)) — prior art: realestate-agent-platform.
- RAG answers over feed + policies with citations.

---

### Phase E — Settlement Flow UI (3–4 h)

**Goal:** one live panel, no static/live duplication.

1. `closing-passport-panel.tsx` — single fetch `/api/demo/closing-passport`.
2. Render: Property Shield · Capital Map · Route Comparison · Bank Counter-Offer · Passport hash · `infrastructure_context`.
3. `use-demo-fetch.ts` + `api-base-url.ts` (`NEXT_PUBLIC_SEABW_API_URL` ?? `NEXT_PUBLIC_BANKABLE_API_URL`).

**Gate:** scroll demo shows routes; hash visible; API down → clear error message.

**Expand quality:**
- Role-based views (banker / compliance / buyer).
- Animated timeline; bank counter-offer memo from LLM (schema-bound).
- SWR/cache; API health indicator in header.

---

### Phase F — Guided simulation + evidence export (2 h)

1. `GET /api/demo/guided-simulation` — 6 steps: pressure → review → shield → bank → compliance → passport.
2. `GET /api/demo/evidence-pack` — privacy-safe JSON export.
3. UI: `guided-deal-simulation.tsx` with link to evidence JSON.

**Expand quality:**
- WebSocket step progression; presenter mode.
- Signed export URLs; audit log.

---

### Phase G — Scenario matrix (3–4 h)

1. Eight scenarios in `scenarios.json` (capital, property, agent, developer supply paths — see [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md)).
2. `services/scenarios.py` — list, detail, run with `bank_action`, `supply_risk_signals`, + `rag_trace` stub.
3. Endpoints: `/api/scenarios`, `/api/scenarios/{id}`, `/api/scenarios/{id}/run`, `/api/scenarios/{id}/rag-run`.
4. UI: `scenario-simulator.tsx` with labels for all scenario ids.
5. Supplier contrast: `GET /api/demo/supplier-contrast`, `supplier-contrast-demo.tsx` (v0.5.5).

**Gate:** green/amber/red/escalate outcomes match [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md).

**Expand quality:**
- Add scenarios without code changes (data-only).
- Bank-specific policy packs.
- Closing Passport hash per scenario (already stubbed for some).

---

### Phase H — RAG layer (optional, 4–8 h)

See [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) for start order and smoke commands. Tier matrix: [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md).

1. `infra/docker-compose.yml` — Qdrant.
2. `services/rag.py` — ingest `data/synthetic/**` via rglob; embedding + reranker HTTP clients.
3. `POST /api/rag/ingest`, `GET /api/rag/health`; scenario `rag-run?mode=auto|fallback|live`.
4. **Explicit fallback** when services down — log + UI label (no silent degradation).

**Gate:** ingest dry_run; usdt-mixed-route returns retrieved_evidence or fallback reason.

**Expand quality:**
- Hybrid dense+sparse (BGE-M3).
- ColBERT rerank; citation spans in UI.
- Per-tenant collections.

---

### Phase I — Vision extensions (2–3 h each)

| Module | API | UI | Expand |
|--------|-----|-----|--------|
| Yield OS | `/api/demo/post-closing-yield-plan` | `post-closing-yield-plan.tsx` | Real manager marketplace, rental income accounts |
| Pitch | static | `pitch-screen.tsx` | Judge mode; localized TH/EN |
| Web3 attestation | metadata in evidence attestation | explain in pitch | Testnet tx; registry API |

---

### Phase J — Buyer consultation agent (optional, 6–12 h)

See [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md), [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md), [`AGENT_STACK_EVALUATION.md`](AGENT_STACK_EVALUATION.md). Local contour: [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md).

1. Create `apps/buyer-agent/` — pnpm + TypeScript + `@langchain/langgraph` + `zod`.
2. Define Zod state schema (session, property, capital, citations, last_node).
3. Implement nodes: intake, property Q&A, capital Q&A, route exploration, handoff.
4. Wire tools to FastAPI `:8080` — developer hub, scenario preview, RAG wrapper.
5. LM Studio at `LOCAL_AI_LLM_INSTRUCT_BASE_URL` — schema-bound replies only.
6. Optional: chat panel in `apps/web/src/agent/` with streamed node status.

**Gate:** buyer can jump topics; agent returns cited answers; RED path never suggests deposit.

**Expand quality:**
- LangGraph checkpoint store for suspend/resume.
- Settlement Branch Explorer merged into bank graph (Phase K+).

---

### Phase K — Docs, deploy, handoff (2–4 h)

Minimum doc set for hackathon judges:

- `MONEY_INFRASTRUCTURE_THESIS.md`, `PITCH_SCRIPT.md`, `DEMO_CHECKLIST.md`, `HACKATHON_RUNBOOK.md`
- `DEPLOY.md`, `PUBLISH_SEABLOCKCHAINWEEK.md` (if public URL)
- `AGENTS.md`, `HANDOFF.md`, `CHANGELOG.md`

Deploy API (Docker/Render) **before** building static site with `NEXT_PUBLIC_SEABW_API_URL`.

---

## 5. Module expansion matrix

Use this when prioritizing quality vs new features:

| Layer | MVP (hackathon) | +Quality | +Functionality |
|-------|-----------------|----------|----------------|
| Developer Knowledge | Static JSON feed | Freshness SLA, validation | ERP sync, agent channels |
| Property Shield | Rule flags on case | Configurable policy engine | External KYC/title signals |
| Capital Map | green/amber/red | Source-of-funds scoring | Bank API verification |
| Route Comparison | 3 routes, escrow win | Scored routes + memos | Live SWIFT/crypto rails |
| Closing Passport | SHA256 hash, no PII | PDF + QR | On-chain attestation registry |
| Scenarios | 6 synthetic paths | Data-driven new scenarios | Production case intake |
| RAG | Qdrant + fallback | Rerank + citations | Bank-private deployment |
| Buyer agent | Doc spec only | LangGraph scaffold | Full consultation + handoff |
| Settlement graph | Linear guided sim | Branch explorer UI | LangGraph bank graph |
| Yield OS | Vision screen | Legal mode detail | Property manager network |

---

## 6. API contract (copy-paste checklist)

Implement and smoke all:

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/api/demo/closing-passport
curl http://localhost:8080/api/demo/developer-knowledge-hub
curl http://localhost:8080/api/demo/supplier-contrast
curl http://localhost:8080/api/demo/guided-simulation
curl http://localhost:8080/api/demo/evidence-pack
curl http://localhost:8080/api/demo/post-closing-yield-plan
curl http://localhost:8080/api/scenarios
curl http://localhost:8080/api/scenarios/swift-clean-route/run
curl http://localhost:8080/api/scenarios/cash-red-route/rag-run
```

Expected anchor invariant:

```bash
# developer hub
knowledge_vs_agent_gap.status == "mismatch_detected"

# closing passport
property_shield.risk_level == "high"
recommended_route.id == "bankable_escrow"
capital_bankability_map["src-p2p"].status == "red"   # id may vary
```

---

## 7. UI demo order (presenter script)

Match [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md):

1. Pitch Screen (thesis, not buyer app)
2. Supplier Contrast (off-platform prelaunch vs tier-1 on-network)
3. Developer Knowledge Hub (upstream mismatch)
4. Anchor case cards
5. **Settlement Flow panel** ← spend most live demo time here
6. Post-Closing Yield Plan
7. Guided Deal Simulation
8. Scenario Simulator (2–3 scenarios incl. supply paths)
9. Evidence Pack JSON
10. Close: SSOT → rails → Passport → Yield OS

3-minute timing: [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md)

---

## 8. Verification gates (Definition of Done)

Before calling MVP complete:

- [ ] `uv run pytest` — target 30+ tests (engines + API + routing edge cases)
- [ ] `pnpm run build` — no TypeScript errors
- [ ] All demo endpoints 200 with API running
- [ ] UI sections load from API (not hardcoded capital/routes)
- [ ] No secrets / TailScale IPs in git
- [ ] `CHANGELOG.md` updated
- [ ] Presenter can run demo offline story from `PITCH_SCRIPT.md` if API fails

---

## 9. Minimal hackathon timeline (24 h)

| Hours | Deliverable |
|-------|-------------|
| 0–4 | Phases A–B: scaffold + anchor + synthetic |
| 4–10 | Phase C–E: engines + closing-passport API + Settlement UI |
| 10–14 | Phase D + F: Developer Hub + guided sim |
| 14–18 | Phase G: scenarios |
| 18–22 | Phase K: pitch screen + docs + deploy |
| 22–24 | Phase H optional RAG; Phase J optional buyer agent; rehearsal |

Your existing repo **already implements Phases A–K** (RAG and buyer agent optional). A new team can skip to extending modules in §5.

---

## 10. Continue development on this repo

If the hackathon starts fresh elsewhere but **you** keep this codebase:

1. Pull latest; read [`HANDOFF.md`](HANDOFF.md) § Next Work.
2. Do not rebuild — extend:
   - **Buyer Consultation Agent** — LangGraph.js scaffold per [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md)
   - Deploy API + scanovich.ai page ([`PUBLISH_SEABLOCKCHAINWEEK.md`](PUBLISH_SEABLOCKCHAINWEEK.md))
   - PDF Closing Passport
   - Live developer feed ingestion
   - Multi-channel agent (roadmap only in MVP)
3. New chat prompt:

```text
Read AGENTS.md and docs/HANDOFF.md and docs/REPRODUCTION_GUIDE.md.
Continue Bankable Property Network from HANDOFF § Next Work.
```

---

## 11. Do not claim (any reproduction)

- Legal title guarantee
- Regulator / government approval
- Agent licensing
- Full production KYC/KYB (integrate later)
- Property NFT ownership
- Live WhatsApp / Telegram / TTS in hackathon MVP

---

## 12. File index — where logic lives

| Concern | Primary files |
|---------|----------------|
| Anchor case | `apps/api/src/app/demo_case.py` |
| Developer SSOT | `data/synthetic/developers/siam-riverside-feed.json`, `services/developer_knowledge.py` |
| Risk / capital / routes | `services/risk_engine.py`, `capital.py`, `routing.py` |
| Passport hash | `services/evidence_pack.py`, `closing_passport_demo.py` |
| Scenarios | `services/scenarios.py`, `data/synthetic/scenarios/scenarios.json` |
| RAG | `services/rag.py`, `infra/docker-compose.yml` |
| Yield vision | `services/yield_plan.py`, `data/synthetic/rental/*` |
| Web shell | `apps/web/src/app/page.tsx` |
| Live settlement UI | `apps/web/src/app/closing-passport-panel.tsx` |
| Fetch pattern | `apps/web/src/lib/use-demo-fetch.ts` |

---

*This guide is the single reproduction source. Update it when adding a new network layer or demo endpoint.*
