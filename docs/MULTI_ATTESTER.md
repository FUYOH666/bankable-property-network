# Multi-attester registry

`SettlementEscrow` trusts multiple attester EOAs via `setAttester(address, bool)`.
Each bank or regulated entity can run its own attester; escrow accepts any
**trusted** attestation that passes schema and field checks.

## Admin API

```solidity
function setAttester(address attester, bool trusted) external onlyOwner;
mapping(address => bool) public trustedAttesters;
```

- Owner adds/removes attesters without redeploying escrow.
- Release and refund paths call `trustedAttesters[attestation.attester]`.
- Untrusted attester → `AttesterNotTrusted` revert.

## Demo: two trusted attesters

Foundry test `test_release_happy_with_second_trusted_attester` in
[`contracts/test/SettlementEscrow.t.sol`](../contracts/test/SettlementEscrow.t.sol):

1. Owner registers `attester` and `attesterB`.
2. Deposit uses primary attester attestation → release succeeds.
3. Attestation signed by `attesterB` (also trusted) → release succeeds on another deal.
4. Rogue attester (not registered) → `AttesterNotTrusted`.

## Integrator checklist

| Step | Action |
|------|--------|
| 1 | Deploy attester service with bank-owned EOA |
| 2 | Owner calls `setAttester(bankAttester, true)` on escrow |
| 3 | Attestations must use `SettlementApproval` schema UID |
| 4 | Monitor `AttesterTrustChanged` events for audit |

## Production notes

- Rotate attester keys via `setAttester(old, false)` then `setAttester(new, true)`.
- Consider timelock/multisig for owner on mainnet.
- Schema UID and EAS contract address are chain-specific — see [`docs/ATTESTATION_SCHEMA.md`](ATTESTATION_SCHEMA.md).
