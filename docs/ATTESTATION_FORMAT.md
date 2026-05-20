# Closing Passport Attestation Format

## Principle

We do not tokenize the property. We tokenize the evidence of a verified settlement process.

The attestation is safe for a public chain, private chain, or bank-controlled registry because it contains only status metadata and a hash of the evidence pack.

## MVP Format

```json
{
  "buyer_bankability_checked": true,
  "developer_risk_reviewed": true,
  "settlement_route_approved": true,
  "escrow_conditions_generated": true,
  "evidence_pack_hash": "0x...",
  "timestamp": "2026-05-19T00:00:00Z",
  "approver_role": "bank_compliance"
}
```

## Evidence Pack Hash

The backend creates a canonical JSON object from:

- case ID;
- risk report;
- capital bankability map;
- recommended settlement route;
- approver role.

Sensitive fields are stripped before hashing.

Excluded examples:

- `passport_number`;
- `email`;
- `phone`;
- `address`;
- `full_name`.

## MVP Storage

For the hackathon MVP, the API returns the attestation object directly and displays it in the Closing Passport screen.

## Pilot Storage

For a two-week pilot, the same object can be anchored to:

- a testnet transaction memo;
- a simple attestation smart contract;
- a bank-controlled append-only registry.

## Production Direction

Production should add:

- schema versioning;
- issuer identity;
- revocation status;
- policy version;
- privacy-preserving proof strategy;
- access-controlled evidence retrieval.
