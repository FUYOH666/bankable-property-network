# Security — AttestRWA

> Threat model + known limitations. Expands in Week 3 after Foundry fuzz +
> slither pass against the deployed `SettlementEscrow.sol`. Today this is
> a planning doc.

## Trust assumptions

| Component | Assumed honest | Assumed potentially malicious |
|-----------|----------------|-------------------------------|
| EAS protocol | Yes | — |
| Anvil / forked local chain | Yes | — |
| Base Sepolia RPC | Yes (best-effort) | — |
| Attester EOA private key | Yes (in HSM in production) | Yes (revocation path mitigates) |
| Buyer wallet | No | Yes |
| Random external caller | No | Yes |
| Developer feed contents | Yes (signed feed in production) | Yes (anchor case is exactly this) |

## Threat scenarios and mitigations

### T1 — Attester key compromise

**Attack:** an adversary steals the attester private key and signs
attestations approving releases to attacker-controlled addresses.

**Mitigations:**

1. Attestations are **revocable**. Owner can call `eas.revoke(uid)`; the
   escrow re-checks `attestation.revocationTime == 0` at release time.
2. Production key in HSM, not raw `.env`. Demo key is the well-known
   Anvil test key — explicitly never to be used on real networks.
3. Attester EOA whitelist on the escrow (`trustedAttesters[address] =
   true`). Compromise of one attester does not affect others.
4. Per-attester rate limits in the attester service (production —
   detect anomalous signing volumes).

### T2 — Replay across deals

**Attack:** adversary takes a valid attestation for `dealId = 0xAAA` and
calls `release(dealId = 0xBBB, attestationUid = sameUid)` to drain a
different deal.

**Mitigation:** escrow `release()` decodes the attestation data and
checks `attDealId == localDealId`. Replay reverts.

### T3 — Frontrun release tx

**Attack:** adversary observes the buyer's `release()` tx in the mempool
and frontrun-replaces the payee address.

**Mitigation:** the payee is read from the **attestation**, not from the
`release()` call args. Frontrunner cannot change which address receives
the funds without forging an attestation (which requires the attester
key — see T1).

### T4 — Expired attestation reused

**Attack:** an old attestation that was once valid is reused after its
expiration.

**Mitigation:** escrow checks `attestation.expirationTime >
block.timestamp` at release time. Expired attestations cannot release.

### T5 — Wrong-schema attestation

**Attack:** attestation made against a different schema is submitted to
escrow.

**Mitigation:** escrow hard-pins `EAS_SCHEMA_UID_SETTLEMENT_APPROVAL` as
an immutable constructor argument. Other schemas fail the
`a.schema == EAS_SCHEMA_UID_SETTLEMENT_APPROVAL` require.

### T6 — Capital classification drift

**Attack:** wallet that was green at attestation time becomes red
afterwards (e.g. sanction list update, mixer interaction). Adversary
calls `release()` after the change.

**Mitigation:** `capitalClass` is a snapshot at attestation time, bounded
by `expiresAt`. Default expiration is 24h, so drift window is narrow.
For high-value deals, attestation can set a shorter `expiresAt`. Long
drifts require re-attestation.

### T7 — Reentrancy on `release()`

**Attack:** malicious payee contract calls back into `release()` to
withdraw twice.

**Mitigation:** escrow uses OpenZeppelin `ReentrancyGuard`. State
(`deals[dealId].released = true`) is set **before** the ERC-20 transfer.
Foundry test `test_release_reentrancy_revert` covers this in Week 2.

### T8 — Wrong payee in developer feed

**Attack:** a malicious developer feed administrator inserts a fake
authorized payee address; attester signs against it.

**Mitigation (production):** signed feeds with developer's known public
key; escrow + attester verify the feed signature. Demo uses synthetic
JSON files in-repo; this is explicitly an integrity assumption in v1.

### T9 — Schema impostor

**Attack:** someone registers a schema with the same fields under a
different UID and tricks the escrow into accepting it.

**Mitigation:** escrow hard-pins the schema UID at deploy time. UIDs are
deterministic (keccak of schema string + resolver + revocable flag), so
there is exactly one canonical UID per schema configuration.

### T10 — Buyer denial-of-service via dust deposits

**Attack:** an adversary deposits 1 wei of USDC for many dealIds to fill
escrow storage and inflate gas.

**Mitigation:** escrow enforces a minimum deposit (`MIN_DEPOSIT`).
Dust deposits revert. (Implementation Week 2.)

### T11 — Sanction list false positive

**Issue:** wallet incorrectly flagged red, deal blocked.

**Mitigation:** `compliance_dsl` rules can include an escalation branch
(`require: capitalClass != red OR humanReviewApproved`). Attester can
request a human review and re-attest if cleared. Demo uses a static
synthetic taint list; production uses Chainalysis / TRM Labs.

### T12 — Front-end key disclosure

**Issue:** real wallet private keys exposed in browser console.

**Mitigation:** wagmi + viem + RainbowKit — keys stay in the user wallet
(MetaMask, Coinbase Wallet, etc.), never reach our backend. Attester
private key only on the attester service host, never in the browser.

## Privacy

- Evidence pack contents stay off-chain; only the `keccak256` hash is on
  the attestation. PII (names, passport numbers, bank statements) never
  reach the chain.
- Attester address is public (intentional).
- Buyer wallet is public (chain default).
- Synthetic demo data has no real PII.

## Audit posture (current)

### Static analysis — Slither

Run via the dev workflow:

```bash
cd contracts
uv tool run --from slither-analyzer slither src/SettlementEscrow.sol \
  --solc-remaps "@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/ @eas/=lib/eas-contracts/contracts/ forge-std/=lib/forge-std/src/" \
  --filter-paths "lib/" \
  --exclude-low --exclude-informational
```

Latest run (2026-05-20): **0 findings** at low / medium / high severity.
The remaining 4 `block-timestamp` warnings from `forge build` are reviewed
explicitly — they apply to hour-scale escrow deadlines where ±13-second
miner manipulation is non-material. They are not security defects in this
context.

### Foundry tests

- **Unit + happy + reject branches:** 28 tests in `test/SettlementEscrow.t.sol`,
  4 in `test/MockUSDC.t.sol` — all green.
- **Fuzz:** `testFuzz_deposit_amount_and_deadline` (256 runs) covers
  amount and deadline edge cases.
- **Mock infra:** `test/MockEAS.sol` provides controlled `Attestation`
  records so all release/refund branches can be exercised
  deterministically.
- **Gas budgets (max):** `release` 118,733 (< 120k target), `refund`
  102,176, `deposit` 176,087.

### Backend pytest

- 62 tests pass: data loading, RAG corpus, wallet taint, compliance DSL,
  attester decision, attester HTTP endpoints, Farcaster Frame endpoints.

### End-to-end on-chain validation

- `scripts/e2e_rwa_flow.sh` (happy path): buyer deposits, attester signs +
  broadcasts EAS attestation, escrow releases to verified payee. Verified
  on the Anvil fork of Base Sepolia with real EAS bytecode at the
  canonical address.
- `scripts/e2e_rwa_reject.sh` (reject path): same flow with the impostor
  `SRL Holding 2026` payee. Attester signs `payeeVerified=false`, escrow
  refuses release, buyer refunds via the attester-signed reject branch.

## What is still not covered (deferred to mainnet pilot)

- Formal STRIDE / DREAD threat model document.
- Gas-DoS analysis on `release()` and `refund()` at extreme calldata.
- MEV-resistant release pattern (commit-reveal or private mempool).
- Production wallet-taint provider (Chainalysis / TRM Labs).
- HSM-backed attester key handling.
- Multi-signature attester (M-of-N).
- Pause / circuit-breaker semantics (deliberately omitted — keep escrow
  immutable for the hackathon).
- External professional audit (Trail of Bits / OpenZeppelin scope) before
  mainnet deploy or first bank pilot.

## Reporting vulnerabilities

This is hackathon-stage code. Production-grade vulnerability handling
ships when we engage the first bank attester pilot in Q4 2026. For now:
open a GitHub issue or email the project maintainer.

## License + audit posture

- Apache-2.0. Source is public.
- Schema UID, escrow address, attester EOA — all public on-chain.
- Code is **not audited** at hackathon submission time. Foundry fuzz +
  slither pass in Week 3 is **not a substitute for a professional audit**.
  Mainnet deploy is gated on a Trail of Bits / OpenZeppelin scope.
