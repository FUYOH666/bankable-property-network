# API Contract — AttestRWA

REST contract for the off-chain attester service. Returns JSON. All
mutating endpoints idempotent by `dealId`.

## Base URL

| Environment | URL |
|-------------|-----|
| Local dev | `http://localhost:8080` |
| Deployed testnet (Week 3) | _(to be set)_ |

## Authentication

Public endpoints (no auth) for hackathon demo. Production deploy adds:

- HMAC signature header on `POST /attest/settlement` (attester ↔ chain
  observer trust boundary).
- Rate limit by IP and by attester EOA.

## Endpoints — current (Week 1)

### `GET /healthz`

Liveness probe. Returns 200 when the service can bind and import its
modules.

```json
{
  "status": "ok",
  "service": "attestrwa-api"
}
```

### `GET /api/demo/closing-passport`

Legacy settlement flow data (basis for attester logic). Will be replaced
by the new attester response in Week 2.

```json
{
  "case": {
    "id": "case-anchor-deposit-mismatch",
    "network_positioning": "bankable_property_network",
    "capital_sources": [...]
  },
  "property_shield": { "risk_level": "high", "flags": [...] },
  "capital_bankability_map": {...},
  "routes": [...],
  "recommended_route": {...},
  "closing_passport": {...},
  "infrastructure_context": {...}
}
```

503 with `Synthetic demo data unavailable` if synthetic data is missing
on disk.

### `GET /api/demo/developer-knowledge-hub`

Returns the upstream developer ERP feed snapshot vs the agent-claimed
payee. Used by the attester to compute `payeeVerified`.

```json
{
  "module": "developer_knowledge_hub",
  "knowledge_vs_agent_gap": {
    "status": "mismatch_detected" | "verified",
    "agent_claimed_payee": "...",
    "developer_authorized_payee": "..."
  },
  "source_of_truth": "developer_erp_feed",
  "channel_roadmap": [...]
}
```

### `GET /api/demo/supplier-contrast`

Off-platform prelaunch vs tier-1 on-network supply contrast. Backend
feed for the attester service (not a UI endpoint anymore).

### `GET /api/demo/evidence-pack`

Returns the privacy-safe evidence pack (no PII, no bank statements, only
status metadata).

### `GET /api/scenarios`

Lists RWA flow scenarios. Will be replaced by 3 RWA scenarios in
Week 1.4 (`happy-bangkok-condo`, `payee-mismatch-srl`,
`capital-red-mixer-touch`).

```json
{
  "data_classification": "synthetic_demo_data",
  "scenarios": [...]
}
```

### `GET /api/scenarios/{scenario_id}/run`

Runs a scenario through the verification pipeline; returns capital
classification, route decision, and RAG trace.

### `GET /api/scenarios/{scenario_id}/rag-run?mode=auto|live|fallback`

Same as `/run` but with extended RAG retrieval trace. `mode=fallback`
forces the deterministic keyword retrieval path (no Qdrant required).

### `GET /api/rag/health`

```json
{
  "collection": "bankable_property_network",
  "qdrant_url_configured": true,
  "embedding_url_configured": true,
  "reranker_url_configured": true,
  "synthetic_document_count": 39,
  "total_document_count": 39,
  "deployment_tier": "demo_local",
  "embedding_tier": "bge-m3",
  "llm_tier": "lm_studio_optional",
  "production_note": "..."
}
```

### `POST /api/rag/ingest?dry_run=true|false`

Indexes the synthetic corpus into Qdrant. `dry_run` returns counts only.

```json
{
  "mode": "dry_run" | "live",
  "document_count": 39,
  "synthetic_document_count": 39,
  "collection": "bankable_property_network",
  "status": "indexed" | "empty"
}
```

## Endpoints — Week 2 (planned)

### `POST /attest/settlement`

Submit a settlement for attestation. Idempotent by `dealId`.

**Request**

```json
{
  "dealId": "0xabcdef...",
  "buyerWallet": "0x1234...",
  "payeeAddress": "0x5678...",
  "tokenAddress": "0x9abc...",
  "amount": "500000000000",
  "propertyId": "project-landmark-tower-unit-2401",
  "jurisdiction": "TH",
  "expiresInHours": 24
}
```

**Response (approved)**

```json
{
  "decision": "approve",
  "dealId": "0xabcdef...",
  "attestationUid": "0xeeeeee...",
  "attester": "0xf39F...",
  "schemaUid": "0x1f64ec96...",
  "txHash": "0xfeed...",
  "blockNumber": 41754039,
  "easExplorerUrl": "https://base-sepolia.easscan.org/attestation/view/0xeeeeee...",
  "evidence": {
    "evidenceHash": "0xdead...",
    "retrievedDocuments": [...],
    "retrievalMode": "qdrant_embedding_reranker",
    "rerankScoreTop": 0.91
  },
  "capitalClass": "green",
  "payeeVerified": true,
  "explanation": "Payee matches developer feed; wallet history clean; capital green."
}
```

**Response (rejected)**

```json
{
  "decision": "reject",
  "dealId": "0xabcdef...",
  "attestationUid": "0xeeeeee...",
  "reason": "payee_mismatch",
  "evidence": {...},
  "payeeVerified": false,
  "capitalClass": "green",
  "explanation": "Agent-claimed payee SRL Holding 2026 not in developer authorized payees. Refund recommended."
}
```

### `GET /attest/{dealId}`

Lookup attestation status by `dealId`.

```json
{
  "dealId": "0xabcdef...",
  "attestationUid": "0xeeeeee...",
  "decision": "approve",
  "attester": "0xf39F...",
  "createdAt": "2026-05-20T11:25:34Z",
  "expiresAt": "2026-05-21T11:25:34Z",
  "revocationTime": null,
  "onChainState": {
    "released": false,
    "refunded": false,
    "escrowAddress": "0x..."
  }
}
```

### `GET /attest/healthz`

```json
{
  "status": "ok",
  "service": "attestrwa-attester",
  "rpcReachable": true,
  "easSchemaUid": "0x1f64ec96...",
  "attester": "0xf39F...",
  "attesterBalance": "10000.0 ETH (test)"
}
```

## Error format

All errors return RFC 7807-style problem JSON:

```json
{
  "type": "https://docs.attestrwa.io/errors/invalid-deal-id",
  "title": "Invalid dealId",
  "status": 400,
  "detail": "dealId must be a 32-byte hex string."
}
```

| Status | Meaning |
|--------|---------|
| 200 | OK |
| 400 | Validation error |
| 404 | Resource not found (e.g. scenario id, dealId) |
| 409 | Idempotency conflict (e.g. dealId already attested) |
| 500 | Internal error (logged) |
| 503 | Synthetic data unavailable / upstream dependency down |

## CORS

Allowed origins (configurable via `BANKABLE_CORS_ORIGINS`):

- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `https://scanovich.ai`, `https://www.scanovich.ai`
- _(production attestrwa domain — Week 3)_

Methods: `GET`, `POST`, `OPTIONS`. Headers: `*`. Credentials: not allowed.

## Versioning

`v1.0.0-alpha.1` (Week 1). Stable `v1.0.0` after Week 3 submit. Breaking
changes between `*-alpha` and `*-beta` are allowed. Post-1.0 follows
semver.
