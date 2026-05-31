# Layered trust on Base

Pattern for composing **identity eligibility** with **deal settlement**
attestation — without rebuilding KYC.

## Two layers

| Layer | Question | Example provider |
|-------|----------|------------------|
| Eligibility | Is this wallet permitted to participate? | Coinbase Verifications, Shibui (ERC-3643) |
| Settlement | Is this specific payee + deal bank-grade? | AttestRWA `SettlementApproval` |

See RFC: [`rfc/0001-settlement-eligibility-composition.md`](rfc/0001-settlement-eligibility-composition.md).

## Coinbase + AttestRWA (2-of-2)

[Coinbase Verifications](https://github.com/coinbase/verifications) publishes
EAS attestations for account verification on Base.

[spire-labs/base-eas-contracts](https://github.com/spire-labs/base-eas-contracts)
shows L3 apps reading Coinbase attestation status from L2 before executing
swaps.

AttestRWA adds the **deal layer**:

1. Consumer checks Coinbase verification attestation for buyer wallet.
2. Consumer checks `SettlementApproval` for `dealId` + `payeeVerified`.
3. Escrow releases only if both pass.

## Shibui + AttestRWA

[Shibui (EEA)](https://github.com/EntEthAlliance/rnd-rwa-erc3643-eas) answers
*wallet eligible to hold security token?* via `EASClaimVerifier.isVerified`.

AttestRWA answers *payee authorized for this settlement?*

Mock composed demo: [`examples/composed-eligibility-settlement/`](../examples/composed-eligibility-settlement/README.md).

## Implementation status

| Component | Status |
|-----------|--------|
| RFC-0001 draft | Done |
| Mock composed flow script | [`scripts/demo-composed-flow.sh`](../scripts/demo-composed-flow.sh) |
| `SettlementEscrowV2` with built-in Coinbase reader | Backlog — use hook pattern first |

## Production notes

Each layer may use a **different attester**. Revocation and expiry must be
checked independently. Evidence stays off-chain; only hashes on-chain.
