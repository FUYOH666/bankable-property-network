# Scenario Matrix

## Purpose

The scenario matrix shows that Bankable Property Network is not a single scripted demo. It can classify different buyer capital sources, property/developer risk profiles, agent behavior, and settlement routes.

Each scenario is a **branch input** to the Settlement Branch Explorer — parallel routes scored and merged by the bank decision graph. See [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md).

## Scenario Overview

| Scenario | Capital | Property/Developer | Agent | Expected Status | Route |
| --- | --- | --- | --- | --- | --- |
| `swift-clean-route` | Dubai bank SWIFT | Verified project | Verified agent | Green | FET-ready escrow |
| `usdt-mixed-route` | USDT + bank transfer | Verified project | Verified agent | Amber | Wallet review, bank conversion, escrow |
| `cash-red-route` | Cash/P2P | Verified project | Limited agent | Red | Reject or legal escalation |
| `mixed-capital-route` | Bank + USDT + unsupported source | Amber project | Limited agent | Amber/Red split | Partial approval and escalation |
| `developer-suspicious-route` | Bank transfer | Changed legal entity | Verified agent | High property risk | Escrow blocked until payee authority |
| `agent-risk-route` | Bank transfer | Verified project | Pressure and no commission disclosure | Agent risk | Escrow plus agent escalation |

## SWIFT Clean Route

Intent:
- demonstrate the green path.

Inputs:
- buyer has documented Dubai bank funds;
- beneficiary and purpose are clear;
- Thai receiving bank route supports FET-ready settlement;
- developer and agent are verified.

System output:
- capital status: green;
- property status: low risk;
- route: Dubai bank to Thai bank to escrow;
- approval: approve with standard conditions;
- Closing Passport generated.

## USDT Mixed Route

Intent:
- show that stablecoins are not rejected automatically, but must become bankable.

Inputs:
- buyer has USDT holdings;
- wallet history is explainable but not sufficient alone;
- property is verified;
- conversion route is required before settlement.

System output:
- capital status: amber;
- required documents: wallet summary, source explanation, conversion record;
- route: wallet review to bank conversion to escrow;
- approval: conditional approval;
- Closing Passport generated after conversion evidence.

## Cash / P2P Red Route

Intent:
- show that the platform does not route everything.

Inputs:
- buyer proposes cash-like route or local P2P conversion;
- counterparty is unclear;
- source-of-funds trail is weak.

System output:
- capital status: red;
- route: rejected or legal escalation;
- approval: no direct settlement;
- Closing Passport not generated until capital becomes bankable.

## Mixed Capital Route

Intent:
- show partial approval and escalation.

Inputs:
- some bank funds are green;
- USDT is amber;
- unsupported cash-like source is red.

System output:
- capital map: green, amber, red;
- route: approve green portion, conditionally review amber, reject red;
- approval: partial and escalated;
- Closing Passport generated only for approved settlement path.

## Developer Suspicious Route

Intent:
- show property-side risk independent of capital.

Inputs:
- buyer funds are bankable;
- payment instruction payee differs from expected developer;
- legal entity changed;
- buyer is pressured to pay deposit.

System output:
- property risk: high;
- capital status: green;
- route: escrow blocked until payee authority;
- approval: escalate;
- Closing Passport generated only after corrected instructions.

## Agent Risk Route

Intent:
- show agent verification value.

Inputs:
- developer is verified;
- buyer funds are bankable;
- agent pressures for deposit;
- commission disclosure is missing;
- agent has limited history.

System output:
- property risk: medium;
- agent risk: high;
- route: escrow plus agent review;
- approval: conditional;
- Closing Passport records agent risk evidence.

## Prelaunch Off-Platform Route

Intent:
- show developer supply risk before buyer settlement — prelaunch sales without permit.

Inputs:
- buyer funds are bankable (SWIFT);
- project sells units before construction permit / EIA clearance;
- developer is off-network — no verified feed;
- agent markets shell-company payee;
- buyer pressured for prelaunch deposit.

System output:
- property risk: high;
- capital status: green;
- route: `reject_prelaunch_no_permit`;
- approval: escalate / reject;
- Closing Passport: not generated;
- supply signals: `prelaunch_without_permit`, `unauthorized_payee`.

See [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md).

## Tier-1 Landmark Route

Intent:
- show on-network tier-1 developer with verified ERP feed.

Inputs:
- Bangkok Landmark Group (fictional tier-1) on-network;
- permit issued, EIA cleared, licensed sales entity matched;
- authorized payee in feed matches payment instruction;
- buyer capital is SWIFT-clean.

System output:
- property risk: low;
- capital status: green;
- route: approve bankable escrow;
- approval: approve;
- Closing Passport: generated;
- supply signals: `permit_verified`, `authorized_payee_matched`.

See [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md).

## Demo Readiness

The product is demo-ready when at least these three scenarios can be selected and explained:

- `swift-clean-route`;
- `usdt-mixed-route`;
- `cash-red-route`.
