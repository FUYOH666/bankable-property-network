# Guided Deal Simulation Design

## Purpose

The guided simulation turns Bankable Property Network from a pitch page into a believable user workflow. It shows the critical moment before money moves and explains how a banking anchor becomes the trust layer.

Today the simulation is **linear** (six fixed steps). The production target is a **LangGraph.js decision graph** — see [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md).

## Flow

1. **Buyer pressure**: the buyer receives an urgent deposit request from an agent.
2. **Document review**: the system compares expected developer name with payment instruction payee.
3. **Risk flags**: Property Shield highlights payee mismatch, urgency, and missing protection clause.
4. **Bank counter-offer**: the banking anchor recommends a Dubai bank to Thai bank FET-ready escrow route and corrected payee authority.
5. **Compliance approval**: compliance approves the controlled route, not the risky direct deposit.
6. **Closing Passport**: the system generates an evidence pack hash and metadata-only attestation.

## Map to Decision Graph Nodes

| Simulation step | Future graph node |
|-----------------|-------------------|
| 1. Buyer pressure | Intake Agent |
| 2. Document review | Property Shield Agent |
| 3. Risk flags | Property Shield Agent → Risk Aggregator (AMBER/RED) |
| 4. Bank counter-offer | Counter-Offer Agent + Settlement Route Agent |
| 5. Compliance approval | Human gate (interrupt) |
| 6. Closing Passport | Closing Passport Agent |

Nonlinear extensions (not in linear demo): parallel Settlement Branch Explorer routes, Yield Agent for investors, FlowCapture P2P mirror.

## Demo Intent

The simulation should answer six questions quickly:

- Why is the buyer in danger?
- Why should money not move directly?
- Why is the bank useful?
- Why is escrow the recommended route?
- What does the Closing Passport prove?
- Why is Web3 used for auditability instead of ownership?

## Implementation

- Backend endpoint: `/api/demo/guided-simulation`.
- Frontend component: `GuidedDealSimulation`.
- Evidence preview includes document IDs, extracted facts, risk flags, route decision, and approver role.
- Evidence preview excludes sensitive fields: `passport_number`, `email`, `phone`, `address`, `full_name`.

## Boundary

This simulation is not legal advice, real KYC, title verification, or a production compliance decision. It is a synthetic pre-settlement workflow for demo and pilot discussion.

## Related

- [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) — nonlinear buyer layer before settlement graph
- [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md) — target LangGraph node model
