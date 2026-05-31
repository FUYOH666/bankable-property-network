# Pivot — Bankable Property Network → AttestRWA

Visual timeline for contributors landing in one repo with two generations.

## Timeline

```mermaid
flowchart LR
  subgraph phase1 ["2025–2026 Q1 — v0.5"]
    bpn["Bankable Property Network"]
    th["Thailand property B2B settlement"]
    rag["RAG + Closing Passport"]
    consult["Buyer consult / WhatsApp bridge"]
  end

  subgraph pivot ["2026-05 — SEABW"]
    check["Market check: compliance dashboards saturated"]
    rwa["RWA stablecoin settlement gap identified"]
    ship["AttestRWA shipped ~4h AI-assisted"]
  end

  subgraph phase2 ["2026 Q2+ — v1.0"]
    eas["EAS SettlementApproval schema"]
    esc["SettlementEscrow.sol"]
    att["FastAPI attester + Compliance DSL"]
  end

  bpn --> check
  check --> rwa --> ship
  ship --> eas
  rag --> att
```

## What moved where

| v0.5 asset (`archive/v0.5/`) | v1 role |
|------------------------------|---------|
| Payee mismatch detection | Core reject-path demo |
| Capital classification (green/amber/red) | `capitalClass` in EAS schema |
| RAG (Qdrant + BGE) | Compliance evidence engine |
| Closing Passport model | `SettlementApproval` EAS fields |
| Synthetic developer feeds | Attester input SSOT |
| Buyer consult / 8 UI panels | **Archived** — not maintained |

## Tags

| Tag | Meaning |
|-----|---------|
| `v0.5.13` | Last Bankable Property Network release before pivot |
| `v1.0.0` | First AttestRWA hackathon release |

Explore v0.5:

```bash
git checkout v0.5.13
```

Return to AttestRWA:

```bash
git checkout main
```

## Naming

Public brand: **AttestRWA**. Repository: **[FUYOH666/attestrwa](https://github.com/FUYOH666/attestrwa)**.

Historical name `bankable-property-network` redirects to `attestrwa` on GitHub.
