# Developer And Agent Journey

## Goal

Help good developers and agents separate themselves from risky market participants through verifiable behavior.

## Developer Flow

1. Developer publishes canonical feed (inventory, payee, installments) to **Developer Knowledge Hub**.
2. **On-network tier-1** (demo: fictional Bangkok Landmark Group) — full feed, permit issued, authorized payees matched → green settlement path. See [`DEVELOPER_SUPPLY_DEMO.md`](DEVELOPER_SUPPLY_DEMO.md).
3. **Off-platform prelaunch** (demo: Shadow Bay) — sales before permit, no verified feed → bank blocks bankable route.
4. Verified agencies consume SSOT — they do not invent terms for commission capture.
5. Developer submits project profile for settlement layer.
6. System checks legal entity, project profile, payment account, deposit terms, and complaint signals.
7. Developer receives verified, review-required, or blocked status.
8. Verified developers become easier for banking anchors to route settlement to.

## Agent Flow

1. Agent accesses verified developer corpus via hub (roadmap: WhatsApp/Telegram/email channels).
2. Agent submits profile and transaction role.

**Distinct from Buyer Consultation Agent:** verified agencies read SSOT from Developer Knowledge Hub; the buyer-facing consultation agent is discovery-only and calls bank APIs as tools — see [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).

3. System reviews closed deals, complaints, commission disclosure, pressure signals, and document readiness.
4. Property Shield compares agent payment instructions against developer authorized payees.
5. Agent receives verified, limited-history, or risk-review status.
6. Agent status is included in the scenario decision.

## Participant Value

- Good developers gain trust.
- Good agents gain proof of reliability.
- Buyers see fewer hidden risks.
- Banks can distinguish verified participants from risky ones.

## Boundary

Verified status is platform/network evidence, not official government approval.
