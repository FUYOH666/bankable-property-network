# Comparison Evidence — Empirical Verification (May 2026)

Empirical check of claims in [`COMPARISON.md`](COMPARISON.md). Each row cites
primary sources (repos, docs, code search) — not marketing decks.

---

## Hypothesis 1: Tokenization platforms lack public on-chain settlement attestation schema

| Project | Tokenization | Public EAS settlement schema | Evidence |
|---------|--------------|------------------------------|----------|
| **AttestRWA** | No (by design) | **Yes** — `SettlementApproval` UID documented in [`ATTESTATION_SCHEMA.md`](ATTESTATION_SCHEMA.md) | This repo |
| **Centrifuge** | Yes — [centrifuge/protocol](https://github.com/centrifuge/protocol) | **No** — compliance via transfer hooks (ERC-1404), not EAS settlement schema | [Token compliance docs](https://docs.centrifuge.io/developer/protocol/features/token-compliance/): whitelisting, freeze; no EAS schema |
| **Maple** | Yes | **No public OSS** — proprietary contracts | No public repo with EAS settlement schema (search 2026-05) |
| **RealT** | Yes (property) | **No** — proprietary | No OSS settlement attestation layer |
| **Ondo** | Yes | **No public OSS** — mixed open components, no settlement schema | Product docs focus on tokenized treasuries |
| **Polytrade** | Yes | **No public OSS** | Proprietary |

**Verdict:** **Confirmed.** AttestRWA is differentiated by a public, reusable
EAS schema for settlement decisions.

---

## Hypothesis 2: KYC providers do not replace settlement attestation

| Provider | On-chain signal | Scope | Evidence |
|----------|-----------------|-------|----------|
| **Sumsub / Persona** | Off-chain API; optional partner integrations | Identity/KYC | Not in AttestRWA scope — integrate, don't build |
| **Coinbase Verifications** | EAS attestations on Base | Account verification, benefits gating | [coinbase/verifications](https://github.com/coinbase/verifications): identity, not payee/deal |
| **Shibui (EEA)** | EAS + ERC-3643 | Wallet eligibility for security tokens | [rnd-rwa-erc3643-eas](https://github.com/EntEthAlliance/rnd-rwa-erc3643-eas) |
| **AttestRWA** | EAS `SettlementApproval` | Payee authority, capital class, deal evidence | This repo |

**Verdict:** **Confirmed.** KYC/identity answers *who*; AttestRWA answers
*whether this specific stablecoin movement to this payee is bank-grade*.

---

## Hypothesis 3: Property tokenization rarely implements payee verification

| Approach | Payee verification at settlement | Evidence |
|----------|----------------------------------|----------|
| Title tokenization (RealT-class) | Ownership on-chain; payee wire logic off-chain | Legal/title focus, not escrow attestation |
| AttestRWA | **Core** — `payeeVerified` vs developer feed | [`ARCHITECTURE.md`](ARCHITECTURE.md) reject path |
| v0.5 Bankable (archived) | Payee mismatch demo (Thailand property) | [`archive/v0.5/`](../archive/v0.5/) |

**Verdict:** **Confirmed.** Payee verification at stablecoin settlement is
rare; AttestRWA inherits this from v0.5 domain work.

---

## Hypothesis 4: Open source posture

| Project | License | Public contracts | Slither at hackathon stage |
|---------|---------|------------------|----------------------------|
| AttestRWA | Apache-2.0 | Yes | 0 findings ([`SECURITY.md`](SECURITY.md)) |
| Centrifuge protocol | GPL-2.0 | Yes | Audited (production) |
| Shibui | Apache-2.0 | Yes | Foundry tests, EEA R&D |
| Maple / RealT / Ondo / Polytrade | Proprietary / mixed | Partial or none | N/A |

**Verdict:** **Confirmed** on OSS transparency at early stage; **not** a claim
of production audit parity.

---

## Updated capability matrix (with citations)

| Capability | AttestRWA | Centrifuge | Shibui | Coinbase Verify |
|------------|-----------|------------|--------|-----------------|
| Asset tokenization | [PRODUCT_THESIS](PRODUCT_THESIS.md) non-goal | [protocol](https://github.com/centrifuge/protocol) | via ERC-3643 tokens | No |
| Settlement attestation schema (EAS) | [ATTESTATION_SCHEMA](ATTESTATION_SCHEMA.md) | Not found | No (eligibility topics) | No (identity) |
| Payee verification field | `payeeVerified` in schema | Not found | No |
| Programmable escrow | `SettlementEscrow.sol` | [liquidity-pools Escrow](https://github.com/centrifuge/liquidity-pools) | No |
| Bank-as-attester model | [PRODUCT_THESIS](PRODUCT_THESIS.md) | Issuer/TA model | Trusted attesters per topic | Coinbase as attester |

---

## Honest gaps (unchanged)

See [`COMPARISON.md`](COMPARISON.md) § "Honest where we are weaker" — still
accurate: no production audit, mock wallet taint, single attester whitelist,
testnet only.

---

## Recommended COMPARISON.md cross-links

Add at top of `COMPARISON.md`:

```markdown
> Empirical sources: [COMPARISON_EVIDENCE.md](COMPARISON_EVIDENCE.md) (May 2026).
```
