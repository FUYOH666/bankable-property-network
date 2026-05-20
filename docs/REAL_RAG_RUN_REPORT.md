# Real RAG Run Report

## Service Status

Embedding and reranker services were reachable and ready during the run.

Qdrant was started through Docker Compose.

## Ingestion

```text
mode: live
document_count: 23
collection: bankable_property_network
vector_size: 1024
status: indexed
```

## Scenario Runs

```text
swift-clean-route qdrant_embedding_reranker approve generated
usdt-mixed-route qdrant_embedding_reranker conditional_approve generated_after_conversion_evidence
cash-red-route qdrant_embedding_reranker reject not_generated
developer-suspicious-route qdrant_embedding_reranker escalate generated_after_corrected_instructions
```

## Retrieved Evidence Examples

### SWIFT Clean Route

- `documents/clean_developer_profile.md`
- `documents/fet_ready_checklist.md`
- `scenarios/scenarios.json`

### USDT Mixed Route

- `documents/clean_developer_profile.md`
- `scenarios/scenarios.json`
- `projects/projects.json`

### Cash/P2P Red Route

- `documents/cash_p2p_declaration.md`
- `documents/clean_developer_profile.md`
- `projects/projects.json`

### Developer Suspicious Route

- `documents/suspicious_payment_instruction.md`
- `developers/siam-riverside-living.md`
- `cases/anchor-deposit-mismatch/case.json`

## Interpretation

The demo now has a real controlled RAG path:

- synthetic documents are embedded;
- Qdrant stores and searches evidence vectors;
- reranker reorders candidate evidence;
- scenario runner combines deterministic decision logic with retrieved evidence trace;
- UI can show retrieved evidence and fallback mode.

## Fallback

If Qdrant or AI services are unavailable, `/api/scenarios/{scenario_id}/rag-run?mode=fallback` returns an explicit `deterministic_fallback` mode rather than silently pretending live retrieval happened.
