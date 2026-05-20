# Synthetic Data Guide

All demo documents are synthetic and must stay clearly labeled as `synthetic_demo_data`.

## Why Synthetic Data

The hackathon demo should prove the workflow without exposing real buyers, contracts, bank statements, wallets, or developer records.

## Document Set

- `data/synthetic/cases/anchor-deposit-mismatch/case.json`: anchor buyer case.
- `data/synthetic/cases/anchor-deposit-mismatch/payment_instruction_letter.md`: risky deposit instruction.
- `data/synthetic/developers/siam-riverside-living.md`: developer profile and payee authority risk (anchor hub).
- `data/synthetic/developers/shadow-bay-prelaunch.md`: off-platform prelaunch developer (permit pending).
- `data/synthetic/developers/bangkok-landmark-group.md`: fictional tier-1 on-network developer.
- `data/synthetic/developers/shadow-bay-feed.json`, `bangkok-landmark-feed.json`: ERP-style feeds for supplier contrast.
- `data/synthetic/documents/prelaunch_permit_risk_brief.md`, `tier_one_developer_verification_pack.md`: RAG corpus for supply demo.
- `data/synthetic/policies/prelaunch_sales_policy.md`: block settlement until permit verified.
- `data/synthetic/policies/property_settlement_policy.md`: bank policy snippets.
- `data/synthetic/settlement_rules/routes.json`: route options and bank positions.

Full inventory: [`SYNTHETIC_CORPUS.md`](SYNTHETIC_CORPUS.md). AI audit map: [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md).

## RAG Collections

Recommended Qdrant collections:

- `bankable_property_os_policies`;
- `bankable_property_os_developers`;
- `bankable_property_os_risk_cases`;
- `bankable_property_os_settlement_rules`.

Ingestion: `POST /api/rag/ingest` over `data/synthetic/**` (rglob).

## Evidence Pack Rules

Evidence packs may include:

- document IDs;
- extracted facts;
- risk flags;
- route decisions;
- approver role;
- evidence hash.

Evidence packs must not include:

- passport numbers;
- real names;
- raw bank account numbers;
- wallet private keys.

## Fictional entities (do not present as real)

- **Bangkok Landmark Group** — fictional tier-1 developer for on-network demo track.
- **Shadow Bay Prelaunch** — fictional off-platform prelaunch risk case.
