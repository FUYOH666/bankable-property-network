# Verified Developer Knowledge Layer

## Problem

Commission-driven agents often invent or distort property facts — inventory, payment terms, authorized payees — to accelerate deal closure and commission capture.

The developer already holds the truth in ERP systems: unit availability, pricing, installment schedules, and which legal entity may receive deposits. Without a verified upstream knowledge layer, agents operate without accountability and Property Shield sees payee mismatches too late.

## Solution

**Verified Developer Knowledge Layer** — developer feed as single source of truth (SSOT), consumed by verified agencies and platform-connected agents through RAG-backed channels.

```text
Developer ERP feed → Knowledge Hub → Verified agents/channels → Property Shield → Settlement OS
```

Pitch line:

> Discovery agents distort facts because they have no source of truth. The developer does. Bankable Property OS connects verified developer knowledge to bank-grade settlement rails.

## Hackathon MVP (Vision Stub)

The demo includes:

- Synthetic developer feed: [`data/synthetic/developers/siam-riverside-feed.json`](../data/synthetic/developers/siam-riverside-feed.json)
- Policy doc: [`data/synthetic/policies/developer_knowledge_policy.md`](../data/synthetic/policies/developer_knowledge_policy.md)
- API: `GET /api/demo/developer-knowledge-hub`
- UI: Developer Knowledge Hub vision screen

Anchor case illustration: agent payment instruction points to `SRL Holding 2026 Co., Ltd.` while developer feed authorizes only `Siam Riverside Living Co., Ltd.` — **mismatch_detected**.

## Relationship To Property Shield

Property Shield flags payee mismatch and urgency. Developer Knowledge Hub explains **why** the mismatch matters: the agent instruction diverges from the developer canonical feed.

Downstream: Capital Map → Route Comparison → Closing Passport operate on bank-grade rails only after knowledge and settlement alignment.

## AI Stack

Same controlled environment as compliance RAG:

| Component | Role |
|-----------|------|
| Developer feed ingestion | SSOT for inventory, terms, payees |
| BGE embeddings + Qdrant | Retrieval over developer corpus + policies |
| Reranker | Precision for agent/compliance answers |
| Schema-bound LLM | Channel responses with citations — not free-form invention |
| Explicit fallback | Deterministic mode when AI services unavailable |

AI distributes verified facts. AI does not autonomously move money.

## Channel Roadmap (Not Live In Hackathon)

Future distribution channels:

- WhatsApp
- Telegram
- Email
- Web chat
- Voice assistant with TTS (e.g. ElevenLabs)

## Prior Art

Archived reference implementation: [realestate-agent-platform](https://github.com/FUYOH666/realestate-agent-platform)

Features in prior art (roadmap, not ported to hackathon MVP):

- Multi-channel webhooks (WhatsApp, Telegram, LINE)
- DialogOrchestrator with handoff policy
- DomainPack architecture
- Multi-tenant ingestion pipeline
- Layout-based media for floor plans

Bankable Property Network adopts the **developer SSOT + RAG + channels** pattern but connects it to **money infrastructure** (Property Shield, Closing Passport, Yield OS) rather than standalone chatbot sales.

## Buyer Consultation Agent vs Verified Agency Channels

| Channel | Audience | Authority |
|---------|----------|-----------|
| **Buyer Consultation Agent** | Purchaser exploring a deal | Discovery/education only; tools call bank APIs |
| Verified agency (roadmap) | Licensed intermediaries | Read-only from Developer Knowledge Hub; no payee invention |

The consultation agent consumes developer hub data via `get_developer_knowledge_hub()` — same SSOT, different trust boundary. See [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).

## Boundaries

The Developer Knowledge Layer does **not**:

- move money or replace escrow;
- perform KYC/KYB;
- replace developer CRM or ERP;
- license agents (settlement verification is separate);
- guarantee that every agent uses the hub (incentive alignment via verified network).

It **does** provide verified facts upstream of settlement and reduces distortion that leads to payee mismatch, false urgency, and off-rail deposits.

## Network Layer Placement

Layer 1 in Bankable Property Network stack — upstream of Verified Property Layer and Property Shield.

Full lifecycle:

1. Developer Knowledge Hub (SSOT)
2. Property Shield + settlement engines
3. Closing Passport
4. Post-Closing Yield OS

See also: [`MONEY_INFRASTRUCTURE_THESIS.md`](MONEY_INFRASTRUCTURE_THESIS.md)
