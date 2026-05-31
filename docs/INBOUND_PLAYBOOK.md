# Inbound playbook

When someone contacts you about AttestRWA — use this checklist. Synthetic
data only until a regulated pilot is signed.

## Do not promise

- Mainnet deploy without audit
- Bank LOI or named institution partnerships (unless signed)
- Production Chainalysis / live KYC without integration work
- Property title tokenization

## By contact type

| Type | 15-min demo | Deep follow-up |
|------|-------------|----------------|
| **Bank / regulated** | `./scripts/e2e_rwa_reject.sh` (payee mismatch) + show YAML policy | HSM, audit scope, fee-per-attestation SOW |
| **RWA platform** (Centrifuge-class) | [`FOR_INTEGRATORS.md`](FOR_INTEGRATORS.md) + hook cookbook | PR to their repo; read-only EAS integration |
| **EEA / standards** | RFC-0001 + `./scripts/demo-composed-flow.sh` | Joint Base Sepolia demo with Shibui |
| **OSS contributor** | Link to [good first issues](https://github.com/FUYOH666/attestrwa/issues?q=is%3Aissue+label%3A%22good+first+issue%22) | Review policy pack PR |
| **Grant / ecosystem** | README + ecosystem research docs | Apply with public testnet proof |

## Demo commands (local)

```bash
./scripts/demo-mode.sh
./scripts/e2e_rwa_flow.sh
./scripts/e2e_rwa_reject.sh
curl -s http://localhost:8080/attest/healthz | jq .
```

## Links to send

- Repo: https://github.com/FUYOH666/attestrwa
- Integrators: [`FOR_INTEGRATORS.md`](FOR_INTEGRATORS.md)
- 85s video: https://youtube.com/shorts/BipB2qPzZz0
- Schema UID: `0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96`

## After the call

1. Log contact in [`OUTREACH_TARGETS.md`](OUTREACH_TARGETS.md) contact log
2. Open GitHub issue for integration thread if they agree
3. Prioritize Bet #1 or #4 from [`QUANTUM_LEAP_BETS.md`](QUANTUM_LEAP_BETS.md)
