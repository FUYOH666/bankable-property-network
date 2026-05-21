# AI Audit Index — Bankable Property Network

> **Purpose:** single entry point for automated or human reviewers (including AI agents) auditing this hackathon project. Read this file first, then follow links by tier.

```yaml
project_name: Bankable Property Network
operating_layer: Bankable Property OS
first_module: Closing Passport
version: 0.5.13
author: Aleksandr Mordvinov
author_github: https://github.com/FUYOH666
repository_url: https://github.com/FUYOH666/bankable-property-network
demo_url: https://scanovich.ai/seablockchainweek/
demo_note: hackathon_static_vitrine_may_be_removed_post_event
data_classification: synthetic_demo_data
primary_customer: banking_anchor_and_regulated_structures
social_bonus: buyer_deposit_protection_when_infrastructure_works
hackathon_track: SEA Blockchain Week / money infrastructure for Thailand property
repository_folder_note: folder name SCB-money-care-OS is legacy; product name is Bankable Property Network
registration_copy: docs/PROJECT_DESCRIPTION.md
live_code: apps/api (FastAPI), apps/web (Next.js)
roadmap_not_implemented: apps/buyer-agent (LangGraph.js buyer chat, Settlement Branch Explorer UI)
```

---

## 1. What this project is (30 seconds)

Bank-grade **money infrastructure** for Thailand property — not a listing marketplace. Banks and regulated structures verify participants, classify capital, route settlement, control escrow, and record **Closing Passport** evidence before funds move. Developer ERP feeds are upstream SSOT. All demo data is synthetic.

**Do not misclassify as:** PropTech listing app, buyer education chatbot, property tokenization platform, or official SCB/Sansiri partnership.

---

## 2. Live vs roadmap (auditor checklist)

| Capability | Status | Evidence |
|------------|--------|----------|
| Settlement Flow (Property Shield → Closing Passport) | **Live** | `GET /api/demo/closing-passport`, `closing-passport-panel.tsx` |
| Developer Knowledge Hub (payee mismatch) | **Live** | `GET /api/demo/developer-knowledge-hub` |
| Supplier Contrast (off-platform vs tier-1) | **Live** | `GET /api/demo/supplier-contrast`, `supplier-contrast-demo.tsx` |
| Scenario Simulator (8 synthetic paths) | **Live** | `GET /api/scenarios`, `scenario-simulator.tsx` |
| Guided Deal Simulation | **Live** | `GET /api/demo/guided-simulation` |
| Post-Closing Yield Plan (vision) | **Live stub** | `GET /api/demo/post-closing-yield-plan` |
| RAG over synthetic + consult KB corpus | **Live with explicit fallback** | `GET /api/rag/health`, `POST /api/rag/ingest`, `rag-run?mode=fallback` |
| Buyer Consultation Agent chat | **Live with explicit fallback** | API + WhatsApp + web; Landmark KB; USDT/cash pitch; Qdrant + BGE + rerank + LM Studio when configured; `GET /api/consult/contour/healthz`; dialogue matrix **17/17** offline; LangGraph.js orchestration roadmap |
| Settlement Branch Explorer UI | **Roadmap doc only** | `docs/NONLINEAR_DECISION_GRAPH.md` |
| Real developer ERP / permit registry | **Out of scope** | Synthetic JSON feeds only |
| On-chain property ownership | **Not claimed** | Metadata-only evidence attestation only |

---

## 3. Documentation tiers

### Tier A — Authoritative (must agree with each other)

| Doc | Role |
|-----|------|
| [`PROJECT_DESCRIPTION.md`](PROJECT_DESCRIPTION.md) | Hackathon registration copy (EN) |
| [`MONEY_INFRASTRUCTURE_THESIS.md`](MONEY_INFRASTRUCTURE_THESIS.md) | Core problem/solution thesis |
| [`HANDOFF.md`](HANDOFF.md) | Version, API contract, verification log, next work |
| [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) | Latest pytest/build/smoke results |
| [`AGENTS.md`](../AGENTS.md) | AI/coding agent entry: commands, demo order, conventions |
| [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md) | Presenter flow + smoke curls |
| [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md) | All 8 scenario intents and expected outputs |
| [`SYNTHETIC_CORPUS.md`](SYNTHETIC_CORPUS.md) | Synthetic data inventory |
| [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md) | Multi-channel consult adapters (WhatsApp live) |
| [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md) | Consult dialogue regression evidence (17/17) |
| [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) | Full project audit — LIVE vs ROADMAP, backlog |
| [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md) | Shadow Bay vs Bangkok Landmark supplier narrative |

### Tier B — Presenter / pitch

| Doc | Role |
|-----|------|
| [`PITCH_SCRIPT.md`](PITCH_SCRIPT.md) | 60s and 3min scripts |
| [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md) | 3-minute live demo timing |
| [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) | Condensed demo script |

### Tier C — Architecture / expansion

| Doc | Role |
|-----|------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Components, data flow, AI layers |
| [`DEVELOPER_KNOWLEDGE_LAYER.md`](DEVELOPER_KNOWLEDGE_LAYER.md) | Upstream SSOT model |
| [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) | Settlement Branch Explorer spec |
| [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) | Buyer agent spec |
| [`REPRODUCTION_GUIDE.md`](REPRODUCTION_GUIDE.md) | Rebuild from zero |
| [`LOCAL_AI_CONTOUR.md`](LOCAL_AI_CONTOUR.md) | Local Qdrant + BGE + LM Studio |
| [`AI_SERVICE_TIERS.md`](AI_SERVICE_TIERS.md) | Demo vs enterprise AI matrix |

### Tier D — Historical snapshots (may lag Tier A)

| Doc | Note |
|-----|------|
| [`STAFF_REVIEW_0.5.4.md`](STAFF_REVIEW_0.5.4.md) | Pre–0.5.5 review; counts superseded by VALIDATION_REPORT |
| [`DEMO_REHEARSAL_REPORT.md`](DEMO_REHEARSAL_REPORT.md) | Early rehearsal; see VALIDATION_REPORT for current |
| [`REAL_RAG_RUN_REPORT.md`](REAL_RAG_RUN_REPORT.md) | Point-in-time RAG run |

**Conflict rule:** if Tier D disagrees with Tier A on version, scenario count, or endpoints — **Tier A wins**.

---

## 4. Key invariants (automated checks)

```bash
cd apps/api && uv run pytest -q                    # expect 64 passed
cd apps/web && pnpm run build                      # expect success
curl -s http://localhost:8080/healthz              # expect 200
curl -s http://localhost:8080/api/demo/supplier-contrast | jq .module
# expect "supplier_contrast_demo"
curl -s http://localhost:8080/api/scenarios | jq '.scenarios | length'
# expect 8
curl -s http://localhost:8080/api/demo/developer-knowledge-hub | jq .knowledge_vs_agent_gap.status
# expect "mismatch_detected" on anchor case
```

**Anchor case invariant:** payee mismatch — agent claims `SRL Holding 2026 Co., Ltd.` vs developer authorized `Siam Riverside Living Co., Ltd.`

**Supply demo invariant:** fictional tier-1 **Bangkok Landmark Group** — not a real developer endorsement.

---

## 5. Synthetic data map (0.5.13)

```
data/synthetic/
  developers/
    siam-riverside-feed.json      # anchor hub case
    shadow-bay-feed.json          # off-platform, incomplete
    bangkok-landmark-feed.json    # tier-1 on-network (fictional)
  projects/projects.json          # incl. project-shadow-red, project-landmark-tower
  scenarios/scenarios.json        # 8 end-to-end paths
  documents/                      # RAG corpus incl. prelaunch + tier-one packs
  policies/                       # incl. capital_routes_buyer_pitch, thailand_property_reference_links
data/consult_knowledge/realestate-demo/   # project sales KB (consult-only RAG filter: kind=consult_kb)
data/consult_dialogues/                   # dialogue regression fixtures (dialogue_matrix.yaml)
```

All files: `data_classification: synthetic_demo_data`. No real PII, bank statements, or wallet keys in repo.

---

## 6. Naming hierarchy (consistent across docs)

| Name | Meaning |
|------|---------|
| Bankable Property Network | Platform / brand |
| Bankable Property OS | Operating layer (API + rules + demo UI) |
| Closing Passport | First MVP module — evidence hash before funds move |
| Developer Knowledge Hub | Upstream verified developer feed vs agent gap |
| Property Shield | Property/developer/agent risk flags |
| Capital Bankability Map | green / amber / red capital classification |
| Bankable Property & Yield OS | Post-closing vision (rental, managers) |

---

## 7. Claims auditors should reject if found in submissions

- Real Sansiri, SCB, or named Thai developer **partnership/endorsement**
- Live Buyer Consultation via **API + WhatsApp bridge + web fallback** with full local AI contour (Qdrant + BGE + LM Studio, explicit keyword fallback); LangGraph.js orchestration still roadmap
- Property tokenization or on-chain title transfer
- Production ERP or government permit API integration
- TailScale IPs, internal hostnames, or secrets in public docs

---

## 8. UI demo order (matches live app)

1. Pitch Screen  
2. Supplier Contrast  
3. Developer Knowledge Hub  
4. Anchor case cards  
5. Settlement Flow panel  
6. Post-Closing Yield Plan  
7. Guided Deal Simulation  
8. Scenario Simulator  
9. Buyer Consultation (web / API / WhatsApp) — see [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md)

---

## 9. Verification log (reference)

See [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) and [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) — **v0.5.13**: 64 pytest, dialogue matrix 17/17 offline, 46 RAG docs, consult live LLM when contour up.

---

## 10. Related audit docs

- [`DOCS_AUDIT.md`](DOCS_AUDIT.md) — maintainer doc inventory  
- [`FINAL_STATUS_AND_NEXT_ACTIONS.md`](FINAL_STATUS_AND_NEXT_ACTIONS.md) — human status summary
- [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md) — full audit, gaps, backlog  
- [`CHANGELOG.md`](../CHANGELOG.md) — release history  
