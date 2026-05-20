# Project Description — Bankable Property Network

```yaml
audience: hackathon_registration_reviewers
language: en
project: Bankable Property Network
version: 0.5.13
author: Aleksandr Mordvinov
author_url: https://github.com/FUYOH666
data: synthetic_demo_only
primary_customer: banks_and_regulated_structures
ai_audit_entrypoint: docs/AI_AUDIT_INDEX.md
```

> **Use for hackathon registration.** English, stable narrative — safe to copy-paste into platform forms. Update **Links** when repo and live demo URLs are final. For automated project review, start with [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md).

---

## Project Name

**Bankable Property Network**

## Tagline

Bank-grade money infrastructure for Thailand property — verify participants, classify capital, route settlement, and record evidence before funds move.

---

## Problem

Thailand's property market runs on developer-paid commissions with no professional entry barrier. Intermediaries enter deals without verified skills in visa rules, FET requirements, ownership limits, or payee authority. Money often moves through unverified paths and off bankable rails.

Developers hold the truth — inventory, authorized payees, installment terms — but agents and buyers frequently operate on ad hoc instructions. Off-platform prelaunch sales can hide permit gaps and wrong payees. The Kingdom brand promise expects institutional-grade settlement; market reality still allows grey routes and disputed deposits.

---

## Solution

**Bankable Property Network** is the platform vision: a trust and settlement network for property money flow.

**Bankable Property OS** is the operating layer banks and regulated structures use to:

- ingest verified developer knowledge (upstream SSOT from ERP-style feeds);
- flag property and agent risk (Property Shield);
- classify buyer capital (green / amber / red);
- compare settlement routes and recommend bankable escrow;
- generate a **Closing Passport** — privacy-safe evidence of a verified settlement process.

We do **not** tokenize the property. We attest metadata-only evidence that a controlled settlement process occurred. Buyer deposit protection is a **social bonus** when infrastructure works — the primary customer is the banking anchor.

**Strategic extension (vision):** Bankable Property & Yield OS — compliant rental operations and bank-controlled rental income after closing.

---

## Who Benefits

| Stakeholder | Value |
|-------------|--------|
| **Banks / regulated structures** | Capture high-value settlement flow, escrow packages, audit-ready evidence, long-term client relationship |
| **Compliance** | Structured approve / reject / escalate before release; RAG-assisted evidence review |
| **State / brand alignment** | Traceable foreign inflow, fewer grey routes, market quality matching Kingdom positioning |
| **Developers (on-network)** | Publish inventory and payee truth once; reduce agent-invented terms and prelaunch reputational risk |
| **Verified agents** | Read-only consumption of developer facts from the hub |
| **Buyers** | Side effect: avoid irreversible deposits to wrong entities; bankable routes instead of pressure-driven instructions |

---

## What We Demonstrate (Hackathon MVP)

Live demo panels (synthetic data):

1. **Pitch Screen** — structural problem, money OS narrative, developer supply value prop.
2. **Supplier Contrast** — off-platform prelaunch (permit/payee gaps) vs fictional tier-1 developer on-network with verified feed.
3. **Developer Knowledge Hub** — agent payee instruction vs developer authorized feed (mismatch on anchor case).
4. **Settlement Flow** — Property Shield, Capital Bankability Map, Route Comparison, Bank Counter-Offer, Closing Passport (live API).
5. **Post-Closing Yield Plan** — long-term asset operations vision on bank rails.
6. **Guided Deal Simulation** — buyer → bank → compliance → passport workflow.
7. **Scenario Simulator** — multiple synthetic paths (capital, property, agent, developer supply) with RAG trace or explicit fallback.
8. **Buyer Consultation** — live multi-channel API (`POST /api/consult/message`): web panel, WhatsApp booth demo (4-turn arc incl. USDT purchase pitch), curl; Landmark Sukhumvit consult KB; Qdrant + BGE + LM Studio when contour up; never approves deposits. Telegram, Line, email, voice — roadmap adapters ([`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md)).

**Roadmap only (documented, not full UI):**

- LangGraph.js Buyer Consultation graph (`apps/buyer-agent/` not scaffolded)
- Settlement Branch Explorer (parallel route scoring UI)

---

## Technology Overview

| Layer | Stack |
|-------|--------|
| API | Python 3.12+, FastAPI, uv |
| Web | Next.js, TypeScript, pnpm |
| Data | Synthetic JSON + markdown corpus under `data/synthetic/` |
| RAG (optional demo) | Qdrant, BGE-M3 embeddings, reranker; deterministic fallback when services unavailable |
| Agent runtime (roadmap) | LangGraph.js, policy-controlled tools — no autonomous money movement |

AI does **not** decide whether money moves. AI helps regulated structures review evidence faster, with traceability.

---

## Data and Ethics

- All demo data is **synthetic** — no real passports, bank statements, wallets, or contracts.
- Fictional developers and projects (e.g. Bangkok Landmark Group, Shadow Bay Prelaunch) — **not** real developer or bank endorsements.
- SCB and other bank names may appear as pitch examples only; no implied partnership unless explicitly agreed offline.

---

## Links

| Field | Value |
|-------|--------|
| Author | [Aleksandr Mordvinov](https://github.com/FUYOH666) |
| Repository | https://github.com/FUYOH666/bankable-property-network |
| Live demo | https://scanovich.ai/seablockchainweek/ (hackathon static vitrine; may be removed after event) |
| Documentation | See `README.md`, `docs/PITCH_SCRIPT.md`, `docs/HACKATHON_RUNBOOK.md` |

---

## Copy-Paste Blocks (Registration Forms)

### Short description (~280 characters)

Bankable Property Network is bank-grade money infrastructure for Thailand property. We verify developers, agents, and capital, route settlement through bankable escrow, and issue a Closing Passport — evidence before funds move. Primary customer: banks. All demo data is synthetic.

### Medium description (~600 characters)

Thailand property runs on developer commissions with unverified intermediaries — money moves off bankable rails while payee authority and permits go unchecked. Bankable Property Network gives banks an operating layer: verified developer feeds, Property Shield risk flags, capital classification (green/amber/red), settlement routing, and Closing Passport evidence attestation. Our hackathon demo shows supplier contrast (off-platform prelaunch vs on-network tier-1), payee mismatch detection, live settlement flow, and multiple synthetic scenarios with optional RAG. We do not tokenize property — only metadata-safe settlement evidence. Buyer protection is a side effect; banks are the primary customer.

### Problem (one paragraph)

Foreign capital expects institutional-grade property settlement, but the market admits commission-driven intermediaries without skill or payee verification. Developers hold inventory and authorized payee truth, yet agents often invent terms. Prelaunch sales can proceed before permits clear. Money flows outside bank-controlled rails — creating deposit loss, AML exposure, and a gap between Kingdom brand promise and market reality.

### Solution (one paragraph)

Bankable Property OS connects upstream developer SSOT to bank settlement rails: classify capital, score routes, control escrow, and generate a Closing Passport hash only when the path is permitted. Verified agencies consume facts from the Developer Knowledge Hub instead of improvising payment instructions. The network scales evidence review with AI under human compliance gates — AI never autonomously releases funds.

### Impact (one paragraph)

Banks capture and retain high-value cross-border property flow with audit-ready evidence. Compliance teams get structured approve/reject/escalate workflows. On-network developers reduce prelaunch and payee fraud exposure. Buyers benefit indirectly through bankable routes and blocked releases to unauthorized payees. The platform turns a one-time purchase into a long-term regulated money relationship (Yield OS vision).

### Team / author (registration form)

Aleksandr Mordvinov — https://github.com/FUYOH666

### Demo URL (registration form)

https://scanovich.ai/seablockchainweek/

## Related Docs

- [`MONEY_INFRASTRUCTURE_THESIS.md`](MONEY_INFRASTRUCTURE_THESIS.md)
- [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md)
- [`PITCH_SCRIPT.md`](PITCH_SCRIPT.md)
- [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md)
