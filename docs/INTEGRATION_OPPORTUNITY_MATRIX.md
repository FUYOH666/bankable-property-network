# Integration Opportunity Matrix

Framing document for AttestRWA ecosystem research (May 2026).

## Research questions

| # | Question | Success signal |
|---|----------|----------------|
| RQ1 | Who solves **settlement attestation** (not tokenization, not KYC identity)? | Named OSS project with public EAS schema + escrow gate |
| RQ2 | Which open standards accept a **SettlementApproval** plug-in in ≤1 PR? | Maintainer ACK or merged example hook |
| RQ3 | Where is **funding** for attestation infrastructure (Base, EAS, EEA)? | Published grant/RFP with eligible scope |
| RQ4 | Which maintainers are **reachable** for cross-repo demo? | Issue/PR response within 14 days |

## Scope boundaries (do not confuse)

| In scope | Out of scope |
|----------|--------------|
| Payee verification at settlement | Property title tokenization |
| EAS `SettlementApproval` schema | Building a new KYC provider |
| Programmable stablecoin escrow | Issuing our own stablecoin |
| Bank-as-attester business model | Exchange listing negotiations |

## Scoring rubric

Each candidate repo is scored 1–5 on three axes; **Leverage** = Impact × Openness ÷ Effort.

| Axis | 1 | 3 | 5 |
|------|---|---|---|
| **Impact** | Nice narrative | Shared user / standard | Default integration path |
| **Openness** | Proprietary / stale | OSS but inactive | Active OSS + issues welcome |
| **Effort** | Fork + rewrite | Weekend demo | Single PR / config |

## Matrix template (per candidate)

```text
Name:
URL:
Stars / Last push / License:
Overlap: compete | complement | adjacent
Integration hook: (contract, schema, hook, API)
Scores: Impact _ / Openness _ / Effort _
Leverage: _ (Impact×Openness÷Effort)
Maintainer reachability: high | medium | low
Wild idea: (one non-obvious synthesis)
Next action: issue | PR | demo | skip
```

## Priority tiers (initial)

| Tier | Definition | Action |
|------|------------|--------|
| **A** | Direct complement; integration hook exists | Open PR or joint demo within 30 days |
| **B** | Same primitive, different vertical | Share attestation oracle interface RFC |
| **C** | Narrative / funding only | Cite in docs; no code yet |
| **D** | Compete or stale | Monitor only |

## Top candidates (pre-scored)

Full cards: [`ECOSYSTEM_RESEARCH.md`](ECOSYSTEM_RESEARCH.md).

| Project | Tier | Leverage | Integration hook |
|---------|------|----------|-------------------|
| [Shibui (EEA)](https://github.com/EntEthAlliance/rnd-rwa-erc3643-eas) | A | 4.2 | Eligibility topic + settlement topic in one flow |
| [Centrifuge protocol](https://github.com/centrifuge/protocol) | A | 3.8 | Transfer hook reads EAS before epoch settlement |
| [coinbase/verifications](https://github.com/coinbase/verifications) | A | 3.5 | Layered trust: Coinbase verify + bank attestation |
| [spire-labs/base-eas-contracts](https://github.com/spire-labs/base-eas-contracts) | A | 3.3 | Base appchain reads settlement attestation from L2 |
| [ethereum-attestation-service/eas-contracts](https://github.com/ethereum-attestation-service/eas-contracts) | A | 3.0 | PayingResolver for attester fees |
| [AgentEscrow ERC-8183](https://github.com/AgentEscrow8183/agentescrow-erc8183) | B | 2.5 | Evaluator attestation pattern for agent commerce |
| [mintmas/triple-arbiter](https://github.com/mintmas/triple-arbiter) | B | 2.2 | x402 settlement + threat-intel attestation on Base |
| AttestRWA (this repo) | — | — | Reference implementation |

## Deliverables map

| Phase | Document |
|-------|----------|
| 0 | This file |
| 1 | [`ECOSYSTEM_RESEARCH.md`](ECOSYSTEM_RESEARCH.md) |
| 2 | [`STANDARDS_ALIGNMENT.md`](STANDARDS_ALIGNMENT.md) |
| 3 | [`COMPARISON_EVIDENCE.md`](COMPARISON_EVIDENCE.md) |
| 4 | [`QUANTUM_LEAP_BETS.md`](QUANTUM_LEAP_BETS.md) |
| 5 | [`OSS_OPERATING_PLAN_90DAY.md`](OSS_OPERATING_PLAN_90DAY.md) |
| RFC | [`rfc/0001-settlement-eligibility-composition.md`](rfc/0001-settlement-eligibility-composition.md) |
| Outreach | [`OUTREACH_TARGETS.md`](OUTREACH_TARGETS.md) |
