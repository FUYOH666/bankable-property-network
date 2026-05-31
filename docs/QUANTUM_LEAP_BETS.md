# Quantum Leap Bets — Top 5 Leverage Plays

Non-linear options ranked by x10 potential (community, integration, funding).
See [`INTEGRATION_OPPORTUNITY_MATRIX.md`](INTEGRATION_OPPORTUNITY_MATRIX.md).

Last updated: **2026-05-31**.

---

## Ranking

| Rank | Bet | Ladder (slow) | Quantum leap (fast) | Leverage | Horizon |
|------|-----|---------------|---------------------|----------|---------|
| **1** | Shibui + AttestRWA joint demo | Wait for EEA partnership | Weekend Base Sepolia demo: eligible wallet + verified payee + escrow | **10x** | 1 week |
| **2** | Coinbase verify + bank settlement (2-of-2) | Build internal KYC | Compose existing [coinbase/verifications](https://github.com/coinbase/verifications) + `SettlementApproval` | **8x** | 2 weeks |
| **3** | Category creation (RFC + schema listing) | 45 more internal docs | One RFC + EAS Scan page + 90s video + topic tags | **7x** | 2 weeks |
| **4** | Centrifuge hook cookbook | Exchange LOI | Ship `examples/integrate-centrifuge-hook/` + discussion thread | **6x** | 3 weeks |
| **5** | ASEAN Property YAML marketplace | Thailand-only product | Open `data/policies/asean-property-v1.yaml`; contributors fork attesters | **5x** | 30 days |

---

## Bet 1 — Shibui + AttestRWA (highest leverage)

**Why:** Only active OSS neighbor in EAS+RWA space. Orthogonal questions.
EEA credibility.

**Deliverable:** Single script `scripts/demo-composed-flow.sh`:

1. Shibui `isVerified(buyer)` → pass
2. Buyer deposits to `SettlementEscrow`
3. AttestRWA attester signs `SettlementApproval`
4. Escrow releases to verified payee

**Outreach:** Issue on [rnd-rwa-erc3643-eas](https://github.com/EntEthAlliance/rnd-rwa-erc3643-eas).

---

## Bet 2 — Layered trust on Base

**Why:** Coinbase already ships EAS on Base; banks won't replace it — they'll
layer deal attestation on top.

**Deliverable:** `docs/LAYERED_TRUST.md` + optional `SettlementEscrow` branch
requiring Coinbase attestation reader (pattern from
[spire-labs/base-eas-contracts](https://github.com/spire-labs/base-eas-contracts)).

---

## Bet 3 — Own the category name

**Why:** GitHub search shows **zero competitors** for "settlement attestation."
First mover on naming wins discoverability.

**Deliverables:**

- RFC-0001 (published)
- GitHub topics: `settlement-attestation`, `attestrwa`, `rwa-compliance`
- Rename repo → `attestrwa`
- Register schema on Base Sepolia EAS Scan (public link in README)

---

## Bet 4 — Centrifuge integration without permission

**Why:** Centrifuge docs explicitly support pluggable transfer hooks. Read-only
integration needs no bilateral contract.

**Deliverable:** [`examples/integrate-centrifuge-hook/`](../examples/integrate-centrifuge-hook/README.md)
— pseudocode + interface + test vectors.

---

## Bet 5 — v0.5 → v1 vertical wedge

**Why:** Global RWA narrative is crowded; **ASEAN property settlement** is
defensible domain expertise already in `archive/v0.5/`.

**Deliverable:** `data/policies/asean-property-settlement-v1.yaml` — first
marketplace policy pack; CONTRIBUTING.md already welcomes YAML PRs.

---

## Anti-bets (do not spend leverage here)

| Trap | Why skip |
|------|----------|
| Property title tokenization | Legal mess; explicit non-goal |
| Competing with Centrifuge on tokenization | Saturated; wrong layer |
| Building KYC from scratch | Integrate Sumsub/Persona/Coinbase |
| Mainnet without audit | SECURITY.md blockers |
| Reintroducing v0.5 UI panels | Scope creep; archive frozen |

---

## Success metrics (90-day)

| Metric | Target |
|--------|--------|
| External integration discussions opened | ≥ 3 |
| Composed demo (Shibui or Coinbase) | 1 shipped |
| On-chain attestations (Base Sepolia) | ≥ 10 public |
| GitHub stars | 25+ |
| Policy pack PRs from externals | ≥ 1 |

Full operating plan: [`OSS_OPERATING_PLAN_90DAY.md`](OSS_OPERATING_PLAN_90DAY.md).
