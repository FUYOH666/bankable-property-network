# Ecosystem Research — GitHub Sweep (May 2026)

Systematic scan of 42 repositories across six search vectors for AttestRWA
integration, competition, and narrative leverage. Method: GitHub search API,
org filters, topic tags, manual README review.

**Legend:** Overlap = `compete` | `complement` | `adjacent`. Leverage =
Impact × Openness ÷ Effort (each 1–5).

---

## Vector 1 — EAS + settlement

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 1 | [ethereum-attestation-service/eas-contracts](https://github.com/ethereum-attestation-service/eas-contracts) | 309+ | 2026-05 | MIT | complement | SchemaResolver, PayingResolver | 5/5/2 | 12.5 | high | Attester fee on attest via resolver |
| 2 | [ethereum-attestation-service/eas-sdk](https://github.com/ethereum-attestation-service/eas-sdk) | 200+ | 2026-05 | MIT | complement | TS SDK for attester service | 4/5/2 | 10.0 | high | Publish SettlementApproval in SDK examples |
| 3 | [ethereum-attestation-service/easctl](https://github.com/ethereum-attestation-service/easctl) | — | 2026-05 | — | adjacent | Agent-first CLI | 3/4/2 | 6.0 | medium | Attester as verifiable agent |
| 4 | [coinbase/verifications](https://github.com/coinbase/verifications) | 100+ | 2024-08 | MIT | complement | Coinbase-verified EAS schemas | 4/5/3 | 6.7 | medium | 2-of-2: Coinbase ID + bank settlement |
| 5 | [spire-labs/base-eas-contracts](https://github.com/spire-labs/base-eas-contracts) | — | 2026-02 | — | complement | L3 reads L2 EAS attestations | 4/4/3 | 5.3 | medium | Appchain RWA vault gated on settlement attestation |
| 6 | [anvaya-labs/eas-react](https://github.com/anvaya-labs/eas-react) | — | 2024-08 | — | adjacent | React attestation UI | 2/3/2 | 3.0 | low | Embed attestation status in Next.js demo |
| 7 | [eshaan7/subgraph-eas](https://github.com/eshaan7/subgraph-eas) | — | 2024-12 | — | complement | Index attestations | 3/4/2 | 6.0 | medium | Dune + subgraph for SettlementApproval |
| 8 | [mintmas/triple-arbiter](https://github.com/mintmas/triple-arbiter) | — | 2026-04 | — | adjacent | x402 + threat attestation Base | 3/3/3 | 3.0 | low | Capital taint attestation cross-check |
| 9 | [FUYOH666/attestrwa](https://github.com/FUYOH666/attestrwa) | 1 | 2026-05 | Apache-2.0 | — | Reference impl | — | — | — | Category creator |

---

## Vector 2 — RWA compliance

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 10 | [EntEthAlliance/rnd-rwa-erc3643-eas](https://github.com/EntEthAlliance/rnd-rwa-erc3643-eas) | 1 | 2026-05 | Apache-2.0 | complement | Shibui `isVerified(wallet)` | 5/5/3 | 8.3 | high | Joint demo: eligible holder + verified payee |
| 11 | [centrifuge/protocol](https://github.com/centrifuge/protocol) | 50+ | 2026-05 | GPL-2.0 | complement | Transfer hooks, ERC-7540 vaults | 5/5/4 | 6.3 | high | Hook reads SettlementApproval before deposit epoch |
| 12 | [centrifuge/liquidity-pools](https://github.com/centrifuge/liquidity-pools) | 30+ | 2025-01 | GPL-2.0 | complement | ERC7540Vault + Escrow | 4/5/4 | 5.0 | high | Async settlement waits for bank attestation |
| 13 | [centrifuge/sdk](https://github.com/centrifuge/sdk) | — | 2026-05 | — | complement | JS client | 3/5/3 | 5.0 | medium | SDK helper: `getSettlementAttestation(dealId)` |
| 14 | [elohcrypto/Vanguard](https://github.com/elohcrypto/Vanguard) | — | 2025-12 | — | adjacent | ERC-3643 stablecoin | 2/3/4 | 1.5 | low | Compose Shibui + AttestRWA on Vanguard rail |
| 15 | [bensonyangweb3/compliance-gate-pattern-demo](https://github.com/bensonyangweb3/compliance-gate-pattern-demo) | — | 2026-04 | — | adjacent | Compliance-gate-first LLM pattern | 2/3/2 | 3.0 | low | Same gate pattern for attester API |
| 16 | [madeinathens/RWA-Absolute-proof](https://github.com/madeinathens/RWA-Absolute-proof) | — | 2026-02 | — | adjacent | RWA + EAS UID | 2/2/3 | 1.3 | low | Compare evidence hash approaches |

---

## Vector 3 — Base ecosystem

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 17 | [spire-labs/based-stack](https://github.com/spire-labs/based-stack) | — | 2025-11 | — | adjacent | Base L2 stack | 3/4/4 | 3.0 | medium | Settlement attestation on Superchain |
| 18 | [coinbase/verifications](https://github.com/coinbase/verifications) | — | — | MIT | complement | (see #4) | — | — | — | — |
| 19 | [nia-agent-cyber/agent-trust](https://github.com/nia-agent-cyber/agent-trust) | — | 2026-04 | — | adjacent | EAS reputation on Base | 2/3/3 | 2.0 | low | Attester reputation schema |
| 20 | [ethereum-attestation-service/eas-contracts-example](https://github.com/ethereum-attestation-service/eas-contracts-example) | — | 2024-10 | — | complement | Example EAS project | 3/5/2 | 7.5 | high | PR: add SettlementEscrow example |

---

## Vector 4 — Escrow + attestation

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 21 | [AgentEscrow8183/agentescrow-erc8183](https://github.com/AgentEscrow8183/agentescrow-erc8183) | — | 2026-03 | — | adjacent | Evaluator attestation in escrow | 3/4/3 | 4.0 | medium | Map evaluator role → bank attester |
| 22 | [Pratiikpy/Settle](https://github.com/Pratiikpy/Settle) | — | 2026 | — | adjacent | Hash-committed receipts (Solana) | 3/3/4 | 2.3 | low | Cross-chain evidence hash standard |
| 23 | [Aleks-NFT/agent-settlement-protocol](https://github.com/Aleks-NFT/agent-settlement-protocol) | — | — | — | adjacent | Multi-step atomic settlement | 2/3/4 | 1.5 | low | Settlement NFT carries attestation UID |
| 24 | [1sraeliteX/Astrapilot](https://github.com/1sraeliteX/Astrapilot) | — | 2026-05 | — | adjacent | Milestone stablecoin escrow | 3/2/3 | 2.0 | low | ASEAN trade + property corridor |
| 25 | [CoopHive/alkahest](https://github.com/CoopHive/alkahest) | — | active | — | complement | EAS payment statements | 4/4/3 | 5.3 | medium | ERC20PaymentStatement + SettlementApproval |
| 26 | [flip18731/SplitSettl](https://github.com/flip18731/SplitSettl) | — | — | — | adjacent | Split settlement Solidity | 2/2/3 | 1.3 | low | Multi-party payee splits |

*Note: Agroasys/Cotsel referenced in web research; not indexed under GitHub search
queries used — treat as Tier B manual follow-up.*

---

## Vector 5 — Property / ASEAN

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 27 | [archive/v0.5](../archive/v0.5/) (this repo) | — | 2026-05 | Apache-2.0 | complement | Thailand property SSOT | 4/5/1 | 20.0 | — | ASEAN Property YAML policy pack |
| 28 | [isorobo/obsidian-tokenise](https://github.com/isorobo/obsidian-tokenise) | — | 2026-05 | — | adjacent | RWA knowledge vault | 1/3/1 | 3.0 | low | Cite in ASEAN policy docs |
| 29 | RealT (proprietary) | — | — | prop | compete | Property tokenization | — | — | — | Do not integrate — attest settlement only |
| 30 | [centrifuge/tinlake](https://github.com/centrifuge/tinlake) | 40+ | 2023-11 | GPL-2.0 | adjacent | Legacy securitization | 2/4/4 | 2.0 | medium | Pattern: off-chain doc → on-chain proof |

---

## Vector 6 — Agent finance + policy gates

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 31 | [feedoracle/feedoracle-managed-agents](https://github.com/feedoracle/feedoracle-managed-agents) | — | 2026-04 | — | adjacent | Compliance MCP agent | 2/3/3 | 2.0 | low | Attester MCP tool for MiCA/stablecoin risk |
| 32 | [ethereum-attestation-service/transitive-trust-sdk](https://github.com/ethereum-attestation-service/transitive-trust-sdk) | — | 2025-07 | — | complement | Trust chain on EAS | 3/4/3 | 4.0 | medium | Bank attester in trust graph |
| 33 | [buildooor/github-attestation-action](https://github.com/buildooor/github-attestation-action) | — | 2023-08 | — | adjacent | CI → EAS | 1/3/2 | 1.5 | low | CI attests release hash of attester image |
| 34 | [axel-t81/3c-financial-data-eas](https://github.com/axel-t81/3c-financial-data-eas) | — | 2025-02 | — | adjacent | Credit ratings on EAS | 2/3/3 | 2.0 | low | Capital class signal from rating attestation |
| 35 | [settlemint-archive/solidity-attestation-service](https://github.com/settlemint-archive/solidity-attestation-service) | — | 2026-05 | — | adjacent | Consortium EAS | 2/2/3 | 1.3 | low | Private bank chain attestation |

---

## Vector 7 — Indexing, tooling, docs (supporting)

| # | Repo | ★ | Last push | License | Overlap | Hook | I/O/E | Lev | Reach | Wild idea |
|---|------|---|-----------|---------|---------|------|-------|-----|-------|-----------|
| 36 | [ethereum-attestation-service/eas-docs-site](https://github.com/ethereum-attestation-service/eas-docs-site) | — | 2025-08 | — | complement | Official docs | 4/5/2 | 10.0 | high | PR: RWA settlement use case page |
| 37 | [ethereum-attestation-service/eas-indexing-service](https://github.com/ethereum-attestation-service/eas-indexing-service) | — | 2026-03 | — | complement | Indexer | 3/4/3 | 4.0 | medium | Index SettlementApproval fields |
| 38 | [envoy1084/schemacraft-superhack2024](https://github.com/envoy1084/schemacraft-superhack2024) | — | 2026-02 | — | adjacent | Schema devtool | 2/3/2 | 3.0 | low | Visual schema editor for banks |
| 39 | [anvaya-labs/EAS-devtool](https://github.com/anvaya-labs/EAS-devtool) | — | 2024-08 | — | adjacent | Schema explorer | 2/3/2 | 3.0 | low | Bank dashboard for attestations |
| 40 | [GoldDAO/gold-dao](https://github.com/GoldDAO/gold-dao) | — | 2026-05 | — | adjacent | Gold RWA (ICP) | 2/3/4 | 1.5 | low | Different chain — pattern only |
| 41 | [NewEraOracle/faith-protocol-mvp](https://github.com/NewEraOracle/faith-protocol-mvp) | — | 2026-05 | — | adjacent | Institutional credit infra | 2/2/4 | 1.0 | low | Credit attestation composition |
| 42 | [Hashlock-Tech/hashlock-mcp-server](https://github.com/Hashlock-Tech/hashlock-mcp-server) | — | 2026-04 | — | adjacent | Intent escrow MCP | 2/2/3 | 1.3 | low | Escrow intent + attestation gate |

---

## Synthesis

### Blue ocean confirmation

GitHub search `EAS attestation RWA settlement escrow` returns **only this
repository** as a direct hit. Closest OSS neighbors:

- **Shibui** — wallet *eligibility* (ERC-3643), not settlement payee verification
- **Centrifuge** — tokenization + transfer hooks, no public settlement schema
- **Coinbase verifications** — identity, not deal-level settlement

AttestRWA occupies an **empty category**: settlement attestation primitive.

### Recommended integration order

1. Shibui (EEA) — orthogonal layer, Apache-2.0, active
2. Centrifuge transfer hook — example in `examples/integrate-centrifuge-hook/`
3. EAS docs + contracts-example — schema listing and PayingResolver
4. coinbase/verifications + spire-labs — layered trust on Base

### Manual follow-ups (not in GitHub API results)

| Project | URL | Why |
|---------|-----|-----|
| Cotsel | https://github.com/Agroasys/Cotsel | Milestone escrow + attestations on Base/USDC |
| ERC-3643 Association | https://www.erc3643.org | Institutional members; standards body |
| RedStone RWA Report 2026 | https://blog.redstone.finance/2026/03/26/tokenization-rwa-report-2026/ | Compliance landscape |

---

## Maintenance

Re-run sweep quarterly. Update stars/dates via:

```bash
# Example: refresh Shibui metadata
gh api repos/EntEthAlliance/rnd-rwa-erc3643-eas --jq '{stars: .stargazers_count, pushed: .pushed_at, license: .license.spdx_id}'
```

Last updated: **2026-05-31**.
