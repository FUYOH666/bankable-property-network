# Simulation Artifacts

## Purpose

These artifacts make the guided deal simulation feel like a real user workflow while keeping all data synthetic.

## Artifact Set

- `data/synthetic/cases/anchor-deposit-mismatch/agent_pressure_message.md`: buyer-facing pressure from the agent.
- `data/synthetic/cases/anchor-deposit-mismatch/payment_instruction_letter.md`: payee mismatch document.
- `data/synthetic/templates/compliance_approval_memo.md`: bank compliance rationale.
- `data/synthetic/templates/escrow_conditions_draft.md`: bankable release conditions.
- `data/synthetic/templates/evidence_preview.example.json`: what enters and does not enter the evidence pack.
- `data/synthetic/templates/closing_passport.example.json`: metadata-only attestation example.

## Demo Use

The presenter can show the flow as:

1. Agent pressure message creates urgency.
2. Payment instruction creates payee mismatch.
3. Property Shield flags the risk.
4. Compliance memo explains why direct deposit is rejected.
5. Escrow draft shows the bank counter-offer.
6. Evidence preview explains privacy.
7. Closing Passport proves the verified process through a hash.

## Safety Language

Use this line when presenting:

> All documents are synthetic. The evidence pack stores extracted facts, risk flags, and status metadata. It does not put personal data, contracts, bank statements, or passports on-chain.
