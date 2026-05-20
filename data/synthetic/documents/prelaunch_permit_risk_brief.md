# Prelaunch Sales Without Permit — Risk Brief

Data classification: synthetic demo data.

## Summary

Off-platform prelaunch sales often begin before:

- construction permit issuance;
- EIA clearance;
- licensed sales entity registration for the project.

Buyers may pay booking deposits to entities with no verified authority to receive funds for the advertised project.

## Bank policy (demo)

Bankable Property OS blocks bankable settlement when:

- `permit_status` is pending or unknown;
- payee is not in developer authorized feed;
- sales occur outside verified Developer Knowledge Hub.

## Recommended action

Reject or escalate. Do not release escrow until permit and payee authority are verified on-network.
