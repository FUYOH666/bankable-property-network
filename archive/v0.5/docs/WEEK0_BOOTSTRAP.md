# Week 0 Bootstrap — AttestRWA Pivot

> **Goal:** put the v1 branch on the right foundation before the heavy
> surgery of Week 1.

## Status — Week 0 complete and fully autonomous

| Step | Status |
|------|--------|
| Cut branch `v1/attestation-layer` from `main@7148ac5` | Done |
| Create `archive/v0.5/` scaffold + historical README | Done |
| Create `contracts/` skeleton (Foundry src/test/script) | Done |
| Draft new root README with pivot story (`docs/v1/README_DRAFT.md`) | Done |
| Define EAS Schema `SettlementApproval` (`docs/v1/ATTESTATION_SCHEMA.md`) | Done |
| Install Foundry (forge / cast / anvil 1.7.1) | Done |
| Start local Anvil fork of Base Sepolia (port 8545, chainId 84532) | Done |
| Verify EAS contract present on fork at `0x4200…0021` | Done (code length 4121) |
| Register `SettlementApproval` schema on fork via SchemaRegistry | Done |
| Verify schema via `getSchema(uid)` readback | Done |
| Author `scripts/dev-chain.sh` + `scripts/stop-dev-chain.sh` (idempotent) | Done |
| Author `docs/v1/DEV_SIMULATION.md` (full simulation guide) | Done |
| Update `CHANGELOG.md` with pivot entries | Done |
| Update `.env.example` with dev + production modes | Done |

**No manual blocker.** Week 1 can start immediately on the dev chain.

## The one optional manual step (Week 3, not Week 0)

The real-testnet deploy in Week 3 (so we get public BaseScan / Dune /
Farcaster URLs for the hackathon submission) requires you to:

1. Generate a fresh attester wallet with `cast wallet new` (do not reuse
   any wallet you've used elsewhere).
2. Open <https://www.alchemy.com/faucets/base-sepolia> and request 0.01 ETH
   to that address (the wallet UI needs ~60 seconds with the captcha).
3. Send me the address + the faucet tx hash (private key stays in your
   local `.env` only).

That's it for the optional step. Everything between Week 0 and Week 3 runs
on the local fork and needs nothing from you.

If you'd prefer to skip the public-testnet step entirely (e.g. if Alchemy
captchas keep failing), we have a fallback: record a 60-second screen
demo against the local dev chain. SEA Blockchain Week judges usually
accept that, as long as the EAS protocol and addresses are real (which
they are on the fork).

## What happens next (Week 1)

Week 1 starts immediately on top of the dev chain. It will:

1. Big `git mv` of legacy modules into `archive/v0.5/`:
   - `apps/api/src/app/services/buyer_consultation.py` + tests
   - `services/whatsapp-bridge/`
   - `data/consult_knowledge/`, `data/consult_dialogues/`
   - 6 React panels in `apps/web/src/app/`
   - ~45 markdown files in `docs/`
2. Rebrand to **AttestRWA** in `config.py`, `.env.example`, `AGENTS.md`,
   `README.md` (replace draft with the final version from
   `docs/v1/README_DRAFT.md`).
3. Slim `docs/` to 8 files (per plan §7).
4. Extend `data/synthetic/developers/*.json` with `authorizedPayees`
   wallet addresses (mock).
5. Create 3 RWA scenarios in `data/synthetic/scenarios/`:
   `happy-bangkok-condo`, `payee-mismatch-srl`, `capital-red-mixer-touch`.
6. Run full pytest baseline (must stay green; archived tests excluded).
7. Tag `v1.0.0-alpha.1` for the rebrand checkpoint.

## Decisions log (locked Week 0)

| # | Decision | Value |
|---|----------|-------|
| 1 | Brand | AttestRWA |
| 2 | Network | Base Sepolia (chainId 84532) |
| 3 | Stablecoin | Mock USDC ERC-20 (own deployment) |
| 4 | Buyer Consult | Archive to `archive/v0.5/` (not delete) |
| 5 | Timeline | 1–3 weeks "divine" mode |
| 6 | Demo mode | Live testnet + 3 pre-funded deals + 60s backup video |
| 7 | Repo strategy | Branch `v1/attestation-layer` from `main@v0.5.13` |
| 8 | Solidity framework | Foundry (with fuzz + invariants + slither) |
| 9 | EAS contract on Base Sepolia | `0x4200000000000000000000000000000000000021` |
| 10 | Schema revocable | `true` (escrow re-checks `revocationTime == 0`) |
