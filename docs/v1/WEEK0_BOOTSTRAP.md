# Week 0 Bootstrap — AttestRWA Pivot

> **Goal:** put the v1 branch on the right foundation before the heavy
> surgery of Week 1.

## Status

| Step | Status |
|------|--------|
| Cut branch `v1/attestation-layer` from `main@7148ac5` | Done |
| Create `archive/v0.5/` scaffold + historical README | Done |
| Create `contracts/` skeleton (Foundry src/test/script) | Done |
| Draft new root README with pivot story (`docs/v1/README_DRAFT.md`) | Done |
| Define EAS Schema `SettlementApproval` (`docs/v1/ATTESTATION_SCHEMA.md`) | Done |
| Update `CHANGELOG.md` with pivot entry | Done |
| **Manual step:** generate attester wallet, fund on Base Sepolia, register schema | **Pending — see below** |

## Manual step you (Aleksandr) must do before Week 1

This is the only blocker before Week 1 starts. Three sub-steps, ~15 minutes.

### A. Generate the attester wallet (clean, never reused)

```bash
cast wallet new
# capture both the address and the private key
```

If you don't have `foundry` / `cast` installed yet:

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Then run `cast wallet new` again.

### B. Fund the attester wallet with Base Sepolia ETH

Open one of these faucets and request a small amount (0.01 ETH is enough):

- <https://www.alchemy.com/faucets/base-sepolia> (Alchemy, recommended)
- <https://faucet.quicknode.com/base/sepolia> (QuickNode)
- <https://docs.base.org/docs/tools/network-faucets/> (Coinbase canonical list)

Verify the balance:

```bash
cast balance --rpc-url https://sepolia.base.org 0xYOUR_ATTESTER_ADDRESS
```

### C. Register the EAS Schema on Base Sepolia

Follow the steps in [`ATTESTATION_SCHEMA.md` section 2](ATTESTATION_SCHEMA.md#2-registration-on-base-sepolia-manual-week-0).

Paste this exact schema string when prompted:

```text
bytes32 dealId, address attester, address payeeAddress, address tokenAddress, uint256 amount, uint8 capitalClass, bytes32 evidenceHash, string jurisdiction, uint64 expiresAt, bool payeeVerified
```

After registration, send me the **Schema UID** (looks like `0xa1b2...`),
and I will:

1. Add it to `docs/v1/ATTESTATION_SCHEMA.md` section 3.
2. Add it to the new `.env.example` as `EAS_SCHEMA_UID_SETTLEMENT_APPROVAL=`.
3. Wire it into the Solidity escrow constructor in Week 2.
4. Update the README hero table.

### D. Send me

Once the three sub-steps are done, reply with:

```text
Attester address: 0x...
Schema UID:       0x...
Faucet tx (FYI):  0x... (optional, just for the audit trail)
```

I do **not** need the private key — keep it in your local `.env` only.

## What happens next (Week 1)

After you complete steps A–D, Week 1 starts. It will:

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
