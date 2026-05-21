# Roadmap — AttestRWA

## Hackathon pivot (now)

`v1/attestation-layer` branch from `main@v0.5.13`. Three-week sprint.

| Week | Goal | Status |
|------|------|--------|
| **Week 0** | Branch, archive scaffold, EAS schema registered on dev fork, draft README with pivot story, Foundry installed, `scripts/dev-chain.sh` idempotent | **Done** (commits `02e8151`, `58aba55`) |
| **Week 1** | Archive legacy modules to `archive/v0.5/`, rebrand to AttestRWA, slim docs from 53 to 8, extend synthetic data with wallet addresses + 3 RWA scenarios, pytest baseline stays green | **Done** (commits `e799c43`, `cf5ec4e`, tag `v1.0.0-alpha.1`) |
| **Week 2** | `SettlementEscrow.sol` + `MockUSDC.sol` with Foundry tests + slither audit. Attester service (`POST /attest/settlement`, EAS client, wallet taint, compliance DSL). End-to-end happy-path smoke against the dev fork. Tag `v1.0.0-alpha.2` | **Done** (commits `0b8ee1f`, `e78e8e4`, `e9b04af`) |
| **Week 3** | Reject-path E2E (`scripts/e2e_rwa_reject.sh`). Farcaster Frame `/api/frame/attest` (HTML + inline SVG). Dune Analytics query pack (`docs/DUNE_QUERIES.md`). Slither audit pass (0 findings). Expanded threat model. README quickstart. Tag `v1.0.0` | **Done** |

### Week 2 sub-tasks

1. Foundry workspace setup (`forge init`, OpenZeppelin + EAS + forge-std deps, `foundry.toml`, `remappings.txt`, `slither.config.json`).
2. `MockUSDC.sol` — minimal ERC-20 with public mint for demos.
3. `SettlementEscrow.sol` — deposit / release / refund + EAS verification, ReentrancyGuard, NatSpec.
4. Foundry unit tests — happy + 6 reject branches (payee mismatch, capital red, expired attestation, revoked attestation, replay across deals, wrong schema impostor).
5. Foundry fuzz / invariant tests — amount overflow, deadline edge, attestation tampering, reentrancy.
6. Slither audit (zero high / medium), gas report (target: `release()` <120k gas).
7. Deploy script (`forge script Deploy.s.sol`) against the Anvil fork; capture addresses into README hero.
8. Backend attester service: `eas_client.py` (web3.py + EAS ABI), `wallet_taint.py` (mock Chainalysis), `compliance_dsl.py` (YAML rule parser), `attester_service.py` orchestrator, `POST /attest/settlement` endpoint with Pydantic schema-bound response. TDD with pytest.
9. Single-screen UI (`apps/web/src/app/rwa-settlement-live.tsx`): wagmi + viem + RainbowKit, wallet connect, deposit form, live escrow event watcher, attester poll, cinematic transitions.
10. E2E smoke script (`scripts/e2e_rwa_flow.sh`): buyer → escrow.deposit → attester decide → EAS.attest → escrow.release → BaseScan-style assertion.
11. Tag `v1.0.0-alpha.2`.

Deliverables at end of Week 3:

- Public BaseScan link to deployed `SettlementEscrow.sol` (verified).
- Public EAS Scan link to `SettlementApproval` schema and at least 3
  on-chain attestations (one happy, one reject, one expired).
- Public Dune dashboard URL.
- Public Farcaster Frame URL.
- 90-second live demo on Vercel + 60-second backup video.
- `archive/v0.5/` clean handoff to prove the pivot was deliberate.

## Q3 2026 — First exchange integration

After hackathon submit and feedback. Target one of:

- Binance Settlement / RWA pilot — AttestRWA attestations gate RWA
  product listing releases.
- OKX RWA — same shape.
- Bybit RWA — same shape.

Engineering work: production attester service hosted on the partner's
controlled environment; multi-attester support (more than just our test
key); on-chain attester registry contract.

## Q4 2026 — First bank attester pilot

Target a regulated bank in ASEAN (likely Thailand or Singapore — both have
explicit RWA / "permissioned DeFi" sandbox programs in 2026). The bank
becomes the **attester** for cross-border property settlements; AttestRWA
provides the off-chain compliance engine + on-chain primitives.

Engineering work:

- Production-grade attester key management (HSM).
- Live integration with the bank's existing KYC + AML platform (Sumsub,
  Persona, internal Quantexa).
- Production wallet taint via Chainalysis / TRM API.
- Audit + penetration test before pilot.

Commercial work: fee-per-attestation pricing model, attester onboarding
agreement, on-chain attester registry update.

## 2027 — Multi-jurisdiction, mainnet

Expand from one bank in one country to a multi-jurisdiction attester
registry. Move from Base Sepolia → Base mainnet (and potentially Optimism
mainnet for redundancy / different attester operators).

Engineering work:

- Mainnet deploy with full audit (Trail of Bits / OpenZeppelin scope).
- Compliance DSL marketplace — banks publish their rule packs as YAML
  files, RWA platforms pick the rule pack that matches their target
  jurisdiction.
- Multi-token support (USDC, USDT, EURC, JPYC).
- L2 cross-chain message relays (LayerZero / Hyperlane) so an attestation
  signed on Base can be verified on Optimism without re-signing.

## What we are explicitly _not_ planning

- Own L1 / L2.
- Own stablecoin.
- Own tokenization product.
- Own KYC provider.
- Mainnet deploy before a regulated bank signs the first attester
  agreement.
- Aggressive marketing or token launch — AttestRWA is infrastructure, not
  a community-yield play.

## Open research questions

These are deferred to Q4 2026 / 2027:

- Attester slashing / staking — should attesters post a bond against
  fraudulent signatures? EAS does not natively support; would need a
  separate slashing contract.
- Privacy-preserving attestations — ZK-proof of compliance without
  revealing the evidence pack contents. Currently `evidenceHash` is
  enough; ZK-proof is overkill for v1 but interesting long-term.
- Cross-attester portability — can a buyer take an attestation from bank
  A and use it at bank B's escrow? Probably not by default
  (attester whitelisting per-escrow), but composable on opt-in.
