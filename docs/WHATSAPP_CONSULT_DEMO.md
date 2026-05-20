# WhatsApp Consultation Demo

Hackathon booth setup for the **Buyer Consultation** layer over WhatsApp (personal account, synthetic demo only).

## Architecture

```text
WhatsApp user → whatsapp-bridge (:8020) → POST /api/consult/message → bankable-api (:8080)
                                                      ↓
                                            LM Studio (optional explainability)
```

Inbound messages call the same consultation service as the web fallback panel. Money decisions remain on deterministic bank rules; the consultant cites API facts only.

## Prerequisites

- Docker: `infra/docker-compose.yml` — **recommended** (`./scripts/docker-up.sh`)
- Personal WhatsApp account for booth pairing (not WhatsApp Business Cloud API)

See [`DOCKER_QUICKSTART.md`](DOCKER_QUICKSTART.md) for full stack commands.

## Booth setup (once)

1. Start stack:

```bash
./scripts/docker-up.sh
# or: docker compose -f infra/docker-compose.yml up -d --build bankable-api whatsapp-bridge
curl http://localhost:8080/api/consult/healthz
curl http://localhost:8020/healthz
```

2. Open pairing page (auto-refreshes QR): **http://localhost:8020/pair**  
   Do **not** use a stale screenshot — scan within ~20 seconds of load.

3. Scan QR with WhatsApp → **Linked devices** → **Link a device**.

4. Optional — link by phone code (often more reliable than QR):

```bash
# In infra/docker-compose.yml under whatsapp-bridge.environment:
WHATSAPP_PAIR_PHONE: "79001234567"   # your number, digits only, no +
docker compose -f infra/docker-compose.yml up -d --build whatsapp-bridge
curl http://localhost:8020/pair-code
# Phone → Linked devices → Link with phone number → enter code
```

5. Optional: lock to your test chat:

```bash
# set in docker-compose or env
ALLOWED_CHAT_JID=1234567890@s.whatsapp.net
```

5. Send a test message: *"What is the payee mismatch?"* — reply should cite Developer Knowledge Hub facts.

## Troubleshooting «Не удалось связать устройство»

| Cause | Fix |
|-------|-----|
| **Stale QR** (most common) | Open http://localhost:8020/pair — page refreshes every 12s. Scan **immediately** after QR appears. |
| **Corrupt session** | `./scripts/whatsapp-reset-session.sh` then scan again on `/pair`. |
| **Too many linked devices** | Phone → WhatsApp → Linked devices → remove old laptops, keep ≤3. |
| **Multi-device off** | Enable linked devices in WhatsApp settings; update WhatsApp app. |
| **Phone offline** | Keep phone on Wi‑Fi/mobile data during pairing. |
| **Client outdated** | Rebuild: `docker compose -f infra/docker-compose.yml up -d --build whatsapp-bridge` |

Check server-side error:

```bash
curl -s http://localhost:8020/status | python3 -m json.tool
docker compose -f infra/docker-compose.yml logs --tail=30 whatsapp-bridge
```

Look at `last_pair_error` in status JSON.

## Expected answers (4-turn distribution + pitch demo)

Demo inventory is **Landmark Sukhumvit Tower** luxury condominiums in **Bangkok** (Bangkok Landmark Group, tier-1 on-network) — **not** a property marketplace or deep consultation bot.

| Turn | User message | Expected behaviour | Judge line |
|------|--------------|-------------------|------------|
| 1 | «привет» / «hello» | Short welcome; distribution + bank decides money | WhatsApp = channel, not payment authority |
| 2 | «i want buy villa» / «price 2BR?» | Landmark Bangkok condos; honest «not Phuket villas» | Project hook from consult_kb |
| 3 | **«а как покупать? у меня usdt»** | **USDT amber pitch** — conversion evidence, verified payee, FET escrow, Land Dept concept; **no prompt leak** | Product pitch — bank rails, not agent wallet |
| 4 | «Can I wire deposit to agent?» | Developer Hub payee facts + **do not deposit** | Bridge to bank infrastructure |

**30-second pitch (turn 3):** USDT is not a shortcut around the bank — it is amber capital that needs conversion evidence, verified payee, FET, and Land Department registration on bankable rails.

| User message | Must NOT appear |
|--------------|-----------------|
| Any project FAQ | `project-riverside`, Dubai inventory, Karon/309 legacy |
| USDT / capital pitch | `cite bank API`, `Settlement/money questions`, raw SYSTEM_PROMPT fragments |

Run dialogue regression before booth:

```bash
cd apps/api && uv run python ../../scripts/run_consult_dialogue_matrix.py --offline
```

After KB changes, re-ingest: `curl -X POST http://localhost:8080/api/rag/ingest`

## 60-second demo script

> This is not a property marketplace chatbot. WhatsApp is how foreign buyers reach **verified developer facts** (Landmark Sukhumvit Tower) and get routed to **bankable settlement** — same API tomorrow on Line or Telegram. We show four turns, not fifty listings.

Project questions use `data/consult_knowledge/realestate-demo/`; settlement questions use bank API facts. One message → one reply (deduplicated). See [`DISTRIBUTION_CHANNELS.md`](DISTRIBUTION_CHANNELS.md).

Fallback: open the **Buyer Consultation (Web Fallback)** panel on the demo site.

## Duplicate replies (fixed in 0.5.7)

If you ever see two identical replies: rebuild bridge after pull — message IDs are deduplicated with a 10-minute TTL. Reset session if needed: `./scripts/whatsapp-reset-session.sh`.

## Security and demo boundaries

| Rule | Detail |
|------|--------|
| Personal account | Hackathon booth only — not production WhatsApp Business |
| Synthetic facts only | No real buyer PII, passports, or bank details in replies |
| Session storage | Docker volume `whatsapp_session/` — **never commit** session DB or QR secrets |
| WhatsApp ToS | Automation on personal accounts may violate Meta ToS — demo risk accepted for expo only |
| No payment actions | Consultant does not approve deposits or trigger escrow |

## Tear-down after event

```bash
docker compose -f infra/docker-compose.yml stop whatsapp-bridge
docker volume rm infra_whatsapp_session   # or project-prefixed volume name
```

Delete local session files if running outside Docker. Rotate/unlink the device in WhatsApp → Linked devices.

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `/qr` returns 503 | Wait for bridge to connect; check `docker logs` for whatsapp-bridge |
| Empty replies | Confirm `BANKABLE_API_URL` reaches API; `curl POST /api/consult/message` |
| Wrong chat answered | Set `ALLOWED_CHAT_JID` |
| LM Studio errors | Expected — template fallback; check API logs for `deterministic_template` |

## Related

- [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md) — full agent roadmap (LangGraph.js)
- [`CONSULT_DIALOGUE_SIMULATION_REPORT.md`](CONSULT_DIALOGUE_SIMULATION_REPORT.md) — multi-turn consult regression
- [`services/whatsapp-bridge/README.md`](../services/whatsapp-bridge/README.md)
