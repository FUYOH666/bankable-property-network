# Docs Audit

> Updated 2026-05-20 — **v0.5.13** · full project audit complete.

## Summary

Documentation aligned with **Bankable Property Network** money infrastructure thesis, live buyer consult (FastAPI + WhatsApp + web), Landmark consult KB, USDT purchase pitch, and nonlinear agent architecture (LangGraph roadmap).

**Master audit:** [`PROJECT_AUDIT_REPORT.md`](PROJECT_AUDIT_REPORT.md)

## Tier A — Authoritative (must match code)

| Doc | Role |
|-----|------|
| `README.md` | Entry, version badge 0.5.13 |
| `CHANGELOG.md` | Release history |
| `docs/AI_AUDIT_INDEX.md` | AI auditor entry — v0.5.13 |
| `docs/PROJECT_DESCRIPTION.md` | Hackathon registration |
| `docs/HANDOFF.md` | Session continuity, context budget |
| `docs/VALIDATION_REPORT.md` | 64 pytest, dialogue 17/17 |
| `docs/PROJECT_AUDIT_REPORT.md` | Full audit artifact |
| `AGENTS.md` | Coding agent commands |
| `docs/DEMO_CHECKLIST.md` | Presenter smoke + flow |
| `docs/SYNTHETIC_CORPUS.md` | 46-doc ingest inventory |
| `docs/DISTRIBUTION_CHANNELS.md` | Multi-channel consult |
| `docs/CONSULT_DIALOGUE_SIMULATION_REPORT.md` | 17/17 dialogue evidence |
| `docs/REAL_RAG_DEMO.md` | RAG + consult LLM paths |

## Tier B — Presenter / pitch

| Doc | Role |
|-----|------|
| `docs/PITCH_SCRIPT.md` | 60s / 3min + 4-turn WhatsApp |
| `docs/HACKATHON_RUNBOOK.md` | Demo arc + USDT turn |
| `docs/WHATSAPP_CONSULT_DEMO.md` | Booth WhatsApp |
| `docs/CONSULT_KNOWLEDGE_DEMO.md` | Consult KB layers |
| `docs/EFFECTIVENESS_SCORECARD.md` | Re-scored 2026-05-20 |
| `docs/NEXT_BUILD_PRIORITY.md` | P0/P1/P2 backlog |

## Tier C — Architecture

| Doc | Role |
|-----|------|
| `docs/ARCHITECTURE.md` | Components + channel adapters |
| `docs/BUYER_CONSULTATION_AGENT.md` | Live FastAPI + LangGraph roadmap |
| `docs/LOCAL_AI_CONTOUR.md` | Qdrant + BGE + LM Studio |
| `docs/REPRODUCTION_GUIDE.md` | Rebuild from zero (version section 0.5.13) |

## Tier D — Historical (may lag)

| Doc | Note |
|-----|------|
| `docs/STAFF_REVIEW_0.5.4.md` | Pre–0.5.5 counts |
| `docs/DEMO_REHEARSAL_REPORT.md` | Early rehearsal |
| `docs/REAL_RAG_RUN_REPORT.md` | Point-in-time RAG run |

**Conflict rule:** Tier A + PROJECT_AUDIT_REPORT wins over Tier D.

## Re-audit checklist (2026-05-20)

- [x] Tier A docs at **0.5.13** / **64 pytest** / **17/17** matrix
- [x] WhatsApp **live** in developer_knowledge channel_roadmap
- [x] 4-turn WhatsApp arc in runbook + pitch script
- [x] PROJECT_AUDIT_REPORT linked from README + HANDOFF + AI_AUDIT_INDEX
- [x] Landmark consult KB (no Karon legacy in Tier A)
- [ ] Optional: `scripts/audit-docs.sh` for CI drift grep (P1)
