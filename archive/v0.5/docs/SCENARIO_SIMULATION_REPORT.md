# Scenario Simulation Report

> Generated: 2026-05-20 10:31 UTC · synthetic demo data · API v0.5.13

Batch run of all scenario branches for hackathon judges. Source: `scripts/run_scenario_matrix.py --api-url http://localhost:8080`.

## Summary matrix

| Scenario | Capital | Property | Agent | Bank action | Passport |
|----------|---------|----------|-------|-------------|----------|
| `swift-clean-route` | green | low | low | approve | generated |
| `usdt-mixed-route` | amber | low | low | conditional_approve | generated_after_conversion_evidence |
| `cash-red-route` | red | low | medium | reject | not_generated |
| `mixed-capital-route` | mixed | amber | medium | conditional_approve | generated_for_approved_path_only |
| `developer-suspicious-route` | green | high | low | escalate | generated_after_corrected_instructions |
| `agent-risk-route` | green | low | high | escalate | generated_with_agent_risk_evidence |
| `prelaunch-off-platform-route` | green | high | high | escalate | not_generated |
| `tier-one-landmark-route` | green | low | low | approve | generated |

## Capital layer

### `swift-clean-route`

**Story:** Clean SWIFT capital, low property and agent risk — FET-ready escrow approved.

| Field | Value |
|-------|--------|
| Project | Riverside Verified Residence |
| Capital | green |
| Property risk | low |
| Agent risk | low |
| Route decision | `approve_fet_ready_escrow` |
| Bank action | **approve** |
| Closing Passport | generated |
| Supply signals | none |

**Judge line:** Green path — bank may proceed to bankable escrow.

### `usdt-mixed-route`

**Story:** Amber USDT/wallet mix — conditional approval after conversion evidence.

| Field | Value |
|-------|--------|
| Project | Riverside Verified Residence |
| Capital | amber |
| Property risk | low |
| Agent risk | low |
| Route decision | `conditional_wallet_review_then_escrow` |
| Bank action | **conditional_approve** |
| Closing Passport | generated_after_conversion_evidence |
| Supply signals | none |

**Judge line:** Conditional — additional evidence required before release.

### `cash-red-route`

**Story:** Red cash/P2P capital — reject or legal escalation, no Closing Passport.

| Field | Value |
|-------|--------|
| Project | Riverside Verified Residence |
| Capital | red |
| Property risk | low |
| Agent risk | medium |
| Route decision | `reject_or_legal_escalation` |
| Bank action | **reject** |
| Closing Passport | not_generated |
| Supply signals | none |

**Judge line:** Reject — do not move funds on this route.

### `mixed-capital-route`

**Story:** Mixed green/amber/red capital — partial approval and escalation.

| Field | Value |
|-------|--------|
| Project | Siam Riverside Living |
| Capital | mixed |
| Property risk | amber |
| Agent risk | medium |
| Route decision | `partial_approval_and_escalation` |
| Bank action | **conditional_approve** |
| Closing Passport | generated_for_approved_path_only |
| Supply signals | none |

**Judge line:** Conditional — additional evidence required before release.


## Counterparty risk

### `developer-suspicious-route`

**Story:** Green capital but payee authority mismatch — escalate until corrected.

| Field | Value |
|-------|--------|
| Project | Siam Riverside Living |
| Capital | green |
| Property risk | high |
| Agent risk | low |
| Route decision | `block_until_payee_authority` |
| Bank action | **escalate** |
| Closing Passport | generated_after_corrected_instructions |
| Supply signals | none |

**Judge line:** Escalate — human compliance review before any release.

### `agent-risk-route`

**Story:** Green capital, high agent pressure — conditional escrow with agent review.

| Field | Value |
|-------|--------|
| Project | Riverside Verified Residence |
| Capital | green |
| Property risk | low |
| Agent risk | high |
| Route decision | `conditional_escrow_and_agent_escalation` |
| Bank action | **escalate** |
| Closing Passport | generated_with_agent_risk_evidence |
| Supply signals | none |

**Judge line:** Escalate — human compliance review before any release.


## Developer supply

### `prelaunch-off-platform-route`

**Story:** Prelaunch sales without permit, off-platform — block bankable route.

| Field | Value |
|-------|--------|
| Project | Shadow Bay Prelaunch |
| Capital | green |
| Property risk | high |
| Agent risk | high |
| Route decision | `reject_prelaunch_no_permit` |
| Bank action | **escalate** |
| Closing Passport | not_generated |
| Supply signals | prelaunch_without_permit, eia_not_cleared, unverified_sales_entity, off_platform_no_hub |

**Judge line:** Escalate — human compliance review before any release.

### `tier-one-landmark-route`

**Story:** Tier-1 on-network developer — green path, Closing Passport generated.

| Field | Value |
|-------|--------|
| Project | Landmark Sukhumvit Tower |
| Capital | green |
| Property risk | low |
| Agent risk | low |
| Route decision | `approve_fet_ready_escrow` |
| Bank action | **approve** |
| Closing Passport | generated |
| Supply signals | permit_verified, eia_cleared, licensed_sales_entity, tier_one_on_network |

**Judge line:** Green path — bank may proceed to bankable escrow.


## Related

- [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md)
- [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)
