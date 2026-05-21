# Developer Supply Demo

> **Audience:** developers / unit suppliers, bank partnership pitch.  
> **Data classification:** synthetic demo only — Bangkok Landmark Group is **fictional tier-1**, not Sansiri/SCB endorsement.

## Why This Demo Exists

Bankable Property Network creates value **before a buyer arrives**. Developers who join publish inventory, authorized payees, and installment terms as the upstream source of truth. Off-platform prelaunch sales hide permit gaps and payee risk — buyers lose deposits before banks can route settlement.

The Supplier Contrast panel shows two tracks side-by-side:

| Track | Developer | Story |
|-------|-----------|-------|
| **A — Without Network** | Shadow Bay Prelaunch (fictional) | Prelaunch sales before construction permit / EIA clearance |
| **B — With Network** | Bangkok Landmark Group (fictional tier-1) | Verified ERP feed, green path, Closing Passport |

## Presenter One-Liners

**RU — off-platform:**

> Покупатель вне сети не видит, что юниты продаются до разрешений. Bankable Property Network подключает SSOT застройщика и блокирует bankable route, пока permit и payee не verified.

**RU — tier-1:**

> Bangkok Landmark Group в сети: inventory, payee и installment terms из ERP feed — агент не может придумать условия, банк видит green path и Closing Passport.

**EN — off-platform:**

> Off-network buyers cannot see prelaunch sales before permits. The network connects developer SSOT and blocks the bankable route until permit and payee are verified.

**EN — tier-1:**

> Bangkok Landmark Group on-network: inventory, payee, and installment terms from the ERP feed — agents cannot invent terms; the bank sees a green path and Closing Passport.

## Track A (3 min) — Buyer Without Network

**Scenario:** `prelaunch-off-platform-route` · **Project:** `project-shadow-red`

1. Open **Supplier Contrast** panel (after Pitch Screen, before Developer Knowledge Hub).
2. Left column: Shadow Bay Prelaunch — permit pending, EIA pending, prelaunch sales active.
3. Point out: no authorized payee in feed, agent marketing payee is a shell entity.
4. Run scenario in Simulator or cite API: `GET /api/scenarios/prelaunch-off-platform-route/run`.
5. Expected output:
   - `property_risk`: high
   - `bank_action`: escalate / reject path
   - `route_decision`: `reject_prelaunch_no_permit`
   - `closing_passport_status`: `not_generated`
   - `supply_risk_signals`: includes `prelaunch_without_permit`

**Synthetic assets:**

- `data/synthetic/developers/shadow-bay-feed.json`
- `data/synthetic/developers/shadow-bay-prelaunch.md`
- `data/synthetic/documents/prelaunch_permit_risk_brief.md`
- `data/synthetic/policies/prelaunch_sales_policy.md`

## Track B (3 min) — Tier-1 On-Network

**Scenario:** `tier-one-landmark-route` · **Project:** `project-landmark-tower`

1. Right column: Bangkok Landmark Group — permit issued, EIA cleared, licensed sales entity matched.
2. Show feed snapshot: authorized payees, inventory count, installment terms from ERP.
3. Run scenario: `GET /api/scenarios/tier-one-landmark-route/run`.
4. Expected output:
   - `property_risk`: low
   - `bank_action`: approve
   - `closing_passport_status`: `generated`
   - `supply_risk_signals`: includes `permit_verified`

**Synthetic assets:**

- `data/synthetic/developers/bangkok-landmark-feed.json`
- `data/synthetic/developers/bangkok-landmark-group.md`
- `data/synthetic/documents/tier_one_developer_verification_pack.md`
- `data/synthetic/projects/bangkok-landmark-tower.md`

## API

```bash
curl http://localhost:8080/api/demo/supplier-contrast
```

Returns side-by-side `off_platform` and `on_network` tracks with scenario run summaries, permit/EIA status, bank action, and Closing Passport status.

## UI Placement

1. Pitch Screen (includes **Why Developers Join** card)
2. **Supplier Contrast** — `apps/web/src/app/supplier-contrast-demo.tsx`
3. Developer Knowledge Hub (anchor payee mismatch)
4. Rest of money infrastructure flow

## Do Not Claim

- Real Sansiri, SCB, or any named Thai developer endorsement
- Live permit registry integration
- Real ERP connection — all feeds are synthetic JSON

## Related Docs

- [`DEVELOPER_KNOWLEDGE_LAYER.md`](DEVELOPER_KNOWLEDGE_LAYER.md) — upstream SSOT model
- [`SCENARIO_MATRIX.md`](SCENARIO_MATRIX.md) — full scenario catalog
- [`PITCH_SCRIPT.md`](PITCH_SCRIPT.md) — supplier opening block
- [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md) — step 1.5 Supplier Contrast
- [`HACKATHON_RUNBOOK.md`](HACKATHON_RUNBOOK.md) — 45 sec supplier talking point
