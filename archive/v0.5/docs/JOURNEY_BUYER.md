# Buyer Journey — Social Bonus Layer

> **Note:** The buyer is not the primary customer. See `docs/MONEY_INFRASTRUCTURE_THESIS.md`. This journey describes the social bonus when bank-grade money infrastructure works correctly.

## Goal

When settlement runs on bankable rails, a foreign buyer gains clarity before irreversible funds move — as a side effect of infrastructure, not buyer education apps.

## Flow

0. Agent instruction compared against developer ERP feed (Developer Knowledge Hub — upstream).
0.5. **Buyer Consultation Agent** (roadmap) — nonlinear exploration of property, capital, and routes via LangGraph.js; calls bank APIs as tools; does not approve payments. See [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).
1. Buyer finds property on any listing or through an agent.
2. Buyer receives payment instruction or deposit pressure through an unverified path.
3. Bankable Property OS intercepts: capital sources classified as green, amber, or red.
4. Property Shield reviews developer, agent, payment account, and deposit terms.
5. Settlement Routing recommends approve, conditional review, reject, or escalate (Settlement Branch Explorer — see [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md)).
6. Buyer receives a Closing Passport summary on a permitted route.

## Buyer Outcomes

- Green route: proceed through bankable escrow.
- Amber route: provide additional documents.
- Red route: do not move money through the proposed path.

## Buyer Promise

The product does not promise that every property is safe. When infrastructure exists, it helps avoid moving money before the route is verified.

## Primary Customer Reminder

Banking anchor and regulated structures operate the flow. Buyer protection is valuable — but it is the social bonus of money OS, not the reason the OS exists.
