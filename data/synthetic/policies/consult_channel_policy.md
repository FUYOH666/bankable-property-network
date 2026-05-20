# Consult Channel Policy (Synthetic Demo)

`data_classification: synthetic_demo_data`

## Purpose

Defines how **distribution channels** connect to the Buyer Consultation API without duplicating settlement logic.

## Single consult brain

All channels call the same endpoint:

```http
POST /api/consult/message
{ "session_id", "message", "channel" }
```

The `channel` field is metadata for logging and analytics (e.g. `whatsapp`, `web`, `telegram`, `line`, `email`, `voice`).

## Live vs roadmap channels

| Channel | Demo status | Notes |
|---------|-------------|-------|
| Web panel | Live | Next.js fallback chat |
| WhatsApp | Live | Go bridge, QR pairing |
| API / curl | Live | Integration testing |
| Telegram | Roadmap | Bot adapter → same POST |
| LINE | Roadmap | OA webhook → same POST |
| Email | Roadmap | Inbound parse → same POST |
| Voice (ASR/TTS) | Roadmap | Whisper ASR → text → POST |

## Authority boundaries

- Consult **explains** project KB and cites bank API facts.
- Consult **never approves** payments, deposits, or escrow release.
- Settlement decisions remain on deterministic bank rules + human compliance.
- Channel adapters must not add payment instructions not present in API citations.

## Fallback

If LLM or RAG services are unavailable, consult returns explicit template fallback (`retrieval_mode` logged). No silent degradation.

## Related

- `docs/DISTRIBUTION_CHANNELS.md`
- `docs/BUYER_CONSULTATION_AGENT.md`
