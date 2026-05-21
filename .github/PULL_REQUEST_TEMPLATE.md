<!--
Thanks for opening a PR against AttestRWA.

Keep this template; check each box that applies.
-->

## What does this PR do

<!-- 1–3 sentences. What changes, why now. -->

## Type of change

- [ ] Contracts (Solidity)
- [ ] Backend (FastAPI / Python)
- [ ] Frontend (Next.js)
- [ ] Scripts / dev tooling
- [ ] Docs / README
- [ ] CI / GitHub config
- [ ] Other (please describe)

## Verification checklist

- [ ] `cd contracts && forge test` — green locally
- [ ] `cd apps/api && uv run pytest -q` — green locally
- [ ] `slither contracts/src/SettlementEscrow.sol` — zero high/medium findings (or justify in this PR)
- [ ] `./scripts/e2e_rwa_flow.sh` — passes against the local dev fork
- [ ] `./scripts/e2e_rwa_reject.sh` — passes against the local dev fork
- [ ] Updated `CHANGELOG.md` with a new entry
- [ ] No secrets committed: `.env*` only, no real private keys, no TailScale IPs, no internal hostnames
- [ ] Updated affected docs under `docs/` (especially if the public API or schema changed)

## Linked issues / context

<!-- Closes #123, follow-up of #456, etc. -->

## Screenshots / on-chain artefacts (if relevant)

<!-- BaseScan tx, EAS Scan attestation, Vercel preview URL. -->
