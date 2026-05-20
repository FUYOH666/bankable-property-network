# Demo Rehearsal Report

> **Historical snapshot** — early hackathon rehearsal. For current verification use [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) (v0.5.5: 37 pytest, 12 smoke endpoints, 8 scenarios). AI auditors: see [`AI_AUDIT_INDEX.md`](AI_AUDIT_INDEX.md).

## Automated Checks (original pass)

Backend:

```text
uv run pytest
13 passed
```

Frontend:

```text
pnpm typecheck && pnpm build
passed
```

Synthetic JSON:

```text
scenarios, projects, agents, buyers, banks, document catalog validated
```

Lints:

```text
No linter errors found
```

Secret/IP scan:

```text
No real secrets or internal IPs found. Matches were false positives on risk-related strings.
```

## Manual Scenario Simulations (subset)

```text
swift-clean-route green low approve generated
usdt-mixed-route amber low conditional_approve generated_after_conversion_evidence
cash-red-route red low reject not_generated
developer-suspicious-route green high escalate generated_after_corrected_instructions
prelaunch-off-platform-route green high reject_prelaunch_no_permit not_generated
tier-one-landmark-route green low approve generated
```

## Demo Interpretation

### Green Route

Clean SWIFT route from Dubai bank to Thai bank is approved. Closing Passport is generated.

### Amber Route

USDT or mixed capital requires conditional approval and conversion evidence before passport generation.

### Red Route

Cash/P2P or unsupported capital is rejected. Closing Passport is not generated on the risky path.

### Developer Supply (added v0.5.5)

Off-platform prelaunch without permit blocks bankable route. On-network tier-1 feed enables approve + Closing Passport.

## Current status

See [`FINAL_STATUS_AND_NEXT_ACTIONS.md`](FINAL_STATUS_AND_NEXT_ACTIONS.md) and [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).
