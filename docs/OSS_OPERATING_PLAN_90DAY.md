# 90-Day OSS Operating Plan

AttestRWA as Apache-2.0 **infrastructure public good**: banks run attesters,
platforms read EAS, community contributes policy packs. Revenue = attestation
fees + pilot SOWs + grants — not rent on the schema.

**Period:** 2026-06-01 → 2026-08-31  
**North star:** Composable settlement attestation primitive with ≥1 external
integration proof.

---

## Milestones

| Week | Milestone | Deliverable | Metric |
|------|-----------|-------------|--------|
| 1 | Research shipped | Ecosystem docs (this sweep) | 6 docs in `docs/` |
| 1–2 | Repo hygiene | Rename `attestrwa`, topics, PIVOT diagram | Discoverability |
| 2 | Outreach wave 1 | Shibui issue + EAS example PR draft | 1 external thread |
| 3 | Composed demo | Shibui or Coinbase layered trust script | 1 video / script |
| 4 | Centrifuge cookbook | `examples/integrate-centrifuge-hook/` | 1 discussion |
| 6 | Public testnet cadence | Weekly attestation on Base Sepolia | 10+ UIDs |
| 8 | Policy marketplace | `asean-property-settlement-v1.yaml` + good first issues | 1 external PR |
| 12 | Grant applications | Base + EEA follow-on submitted | 2 applications |

---

## Community levers

### Good first issues (create on GitHub)

| Issue title | Skill | Value |
|-------------|-------|-------|
| Add Thailand/SG/MY YAML policy pack | Compliance | Jurisdiction coverage |
| Chainalysis adapter stub for `wallet_taint.py` | Python | Production path |
| Multi-attester registry in `SettlementEscrow` | Solidity | Bank pluralism |
| Dune dashboard from `DUNE_QUERIES.md` | Analytics | Public proof |
| Decode `SettlementApproval` in subgraph | TypeScript | Indexer UX |

### Integration cookbook

- [`examples/integrate-centrifuge-hook/`](../examples/integrate-centrifuge-hook/README.md)
- RFC-0001 composition pattern

### Living demo

- Run `./scripts/demo-mode.sh` weekly; post attestation UID to README or Dune
- Farcaster Frame: `/api/frame/attest` for viral surface
- 90s YouTube demo already exists — link in every outreach message

### Maintainer outreach (not cold spam)

Lead with **working code**: link to e2e scripts, schema UID, Slither clean.
Template: [`OUTREACH_TARGETS.md`](OUTREACH_TARGETS.md).

---

## Funding map (research — verify before apply)

| Source | Type | Fit | Action |
|--------|------|-----|--------|
| **GitHub Sponsors** | Recurring | Maintainer sustainability | Enable on `FUYOH666` or `attestrwa` org |
| **Open Collective** | Transparent donations | "Energy exchange" narrative | Optional parallel to Sponsors |
| **Base ecosystem grants** | Grant | Base Sepolia deployment | Check [base.org/build](https://www.base.org/build) |
| **Optimism retroPGF** | Retro funding | EAS public good infra | If Superchain attestation volume grows |
| **EEA R&D** | Collaboration | Shibui adjacency | Via Issue #1 on Shibui repo |
| **Hackathon → pilot SOW** | Paid pilot | Bank/regulated attester | Fee per attestation post-SEABW |
| **Security audit grant** | Audit subsidy | Pre-mainnet | Pair with Centrifuge/OZ audit norms |

**Open core model:**

| Layer | License | Monetization |
|-------|---------|--------------|
| Schema + escrow contracts | Apache-2.0 | Free |
| Attester service reference | Apache-2.0 | Free |
| Hosted attester (HSM, SLA) | Commercial | Bank pilot fees |
| Custom policy packs | Apache-2.0 YAML | Consulting / SOW |
| Audit + mainnet deploy | — | Grant or pilot funded |

---

## Metrics dashboard

Track weekly in a simple spreadsheet or Dune:

| KPI | Baseline (2026-05-31) | 30-day | 90-day |
|-----|------------------------|--------|--------|
| GitHub stars | 1 | 10 | 25 |
| Forks | 0 | 3 | 8 |
| External contributors | 0 | 1 | 3 |
| Open outreach threads | 0 | 3 | 5 merged/answered |
| Base Sepolia attestations | 0 public | 5 | 20 |
| Policy pack PRs | 0 | 0 | 1 |
| Integration demos | 1 (internal) | 2 | 3 |

---

## Risk register

| Risk | Mitigation |
|------|------------|
| "Another EAS demo" | Bank-attester model + engineering bar in every message |
| Regulatory overclaim | Synthetic data only; pilots in ROADMAP not README |
| No maintainer response | Ship PR first, then ping |
| Scope creep to v0.5 | `archive/v0.5/` frozen; see [`PIVOT.md`](PIVOT.md) |
| Mainnet pressure | Grant-funded audit gate in ROADMAP Q4 |

---

## Document index

| Doc | Purpose |
|-----|---------|
| [INTEGRATION_OPPORTUNITY_MATRIX.md](INTEGRATION_OPPORTUNITY_MATRIX.md) | Framing |
| [ECOSYSTEM_RESEARCH.md](ECOSYSTEM_RESEARCH.md) | 42 repo cards |
| [STANDARDS_ALIGNMENT.md](STANDARDS_ALIGNMENT.md) | EEA / ERC-3643 / EAS / Base |
| [COMPARISON_EVIDENCE.md](COMPARISON_EVIDENCE.md) | Empirical claims |
| [QUANTUM_LEAP_BETS.md](QUANTUM_LEAP_BETS.md) | Top 5 bets |
| [rfc/0001-settlement-eligibility-composition.md](rfc/0001-settlement-eligibility-composition.md) | Integration RFC |
| [OUTREACH_TARGETS.md](OUTREACH_TARGETS.md) | Draft messages |

---

## Review cadence

- **Weekly:** KPI tick + one outreach touch
- **Monthly:** Re-run GitHub sweep (update `ECOSYSTEM_RESEARCH.md`)
- **Quarterly:** Revise this plan
