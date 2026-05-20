# Synthetic Corpus

> AI / hackathon auditors: see [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md) for live vs roadmap and data map.

## Purpose

The synthetic corpus gives Bankable Property Network enough structured demo data to simulate a production-scale trust network without using real personal, bank, property, or legal data.

## Corpus Structure

```text
data/synthetic/
  projects/
  agents/
  buyers/
  banks/
  documents/
  scenarios/
```

## Projects

File: `data/synthetic/projects/projects.json`

- `project-riverside-clean`: clean verified project.
- `project-siam-amber`: amber project with payee authority review.
- `project-shadow-red`: blocked prelaunch project (Shadow Bay — permit pending, prelaunch sales active).
- `project-landmark-tower`: verified tier-1 project (Bangkok Landmark Group — fictional).

## Developer Feeds

- `data/synthetic/developers/shadow-bay-feed.json` — intentionally incomplete off-platform feed.
- `data/synthetic/developers/bangkok-landmark-feed.json` — tier-1 on-network feed with authorized payees.
- Profile markdown: `shadow-bay-prelaunch.md`, `bangkok-landmark-group.md`.

See [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md).

## Agents

File: `data/synthetic/agents/agents.json`

- verified agent;
- limited-history agent;
- risky pressure agent.

## Buyers

File: `data/synthetic/buyers/buyers.json`

- clean SWIFT buyer;
- USDT mixed buyer;
- cash/P2P buyer;
- mixed-capital buyer.

## Banks

File: `data/synthetic/banks/banks.json`

- Dubai originator bank;
- Thai receiving bank;
- Singapore originator bank.

## Documents

File: `data/synthetic/documents/document_catalog.json`

Synthetic document types:

- SPA mock;
- reservation agreement;
- payment instruction;
- bank statement summary;
- wallet summary;
- cash declaration;
- FET checklist;
- escrow terms;
- compliance memo.

## Scenarios

File: `data/synthetic/scenarios/scenarios.json`

End-to-end paths:

- `swift-clean-route`;
- `usdt-mixed-route`;
- `cash-red-route`;
- `mixed-capital-route`;
- `developer-suspicious-route`;
- `agent-risk-route`;
- `prelaunch-off-platform-route` (Shadow Bay prelaunch without permit);
- `tier-one-landmark-route` (Bangkok Landmark Group tier-1 on-network).

## Data Safety

All files are marked as synthetic demo data. The corpus contains summaries, IDs, statuses, and mock facts. It must not contain real passports, real bank statements, real wallet owner data, real contracts, or real personal data.
