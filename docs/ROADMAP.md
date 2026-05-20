# Roadmap

## 24-Hour Demo

- One anchor case illustrating infrastructure failure: unverified settlement path, Dubai bank + USDT capital, Thai condo deposit, commission-model context.
- Developer Knowledge Hub (developer ERP feed vs agent payee mismatch).
- Property Shield report.
- Capital Bankability Map.
- Settlement Route Comparison.
- Bank Counter-Offer with FET-ready escrow path.
- Human approval step.
- Evidence pack hash.
- Closing Passport output.
- Guided Deal Simulation.
- Evidence Pack JSON export.
- Documentation pack for demo, roadmap, synthetic data, architecture, stakeholder value, and network positioning.

## 2-Week Pilot

- **Buyer Consultation Agent** scaffold: `apps/buyer-agent/` with LangGraph.js, LM Studio local LLM, policy-controlled tools calling FastAPI. See [`BUYER_CONSULTATION_AGENT.md`](BUYER_CONSULTATION_AGENT.md).
- Developer feed ingestion stub: synthetic ERP snapshot, authorized payees, inventory and installment terms.
- Verified developer and agent profile stubs.
- Richer synthetic document generator for property, agent, developer, and payment instruction scenarios.
- Qdrant collections for policies, developers, risk cases, and settlement rules.
- RAG trace stub showing which synthetic documents informed the decision.
- Configurable policy rules.
- Buyer, banker, and compliance role-based views.
- PDF export for evidence pack.
- Testnet attestation transaction.

## 6-Week Bank Pilot

- **Settlement Branch Explorer** — LangGraph decision graph with parallel route branches, scoring, and human gates. See [`NONLINEAR_DECISION_GRAPH.md`](NONLINEAR_DECISION_GRAPH.md).
- Integration with bank document intake.
- FET-ready settlement checklist.
- Escrow workflow and conditional release controls.
- Compliance workflow permissions.
- Bank officer dashboard.
- Internal audit dashboard.
- Legal review of escrow wording.
- Sandbox integration with wallet analytics or payment rails.
- Pilot metrics dashboard.

## Network Phase

- Verified Developer Knowledge Layer: developer ERP SSOT feed + multi-channel agent distribution (WhatsApp, Telegram, email, voice/TTS) over RAG — prior art from realestate-agent-platform.
- Multi-bank anchors across Thai, Dubai, Singapore, and international settlement participants.
- Verified Property Layer.
- Verified Developer Layer.
- Verified Agent Layer.
- Buyer Capital Layer.
- Settlement Routing Layer.
- Escrow and Conditional Release.
- Closing Passport attestation registry.
- Post-Purchase Financial Layer: rental income accounts, insurance, maintenance payments, tax reminders, resale support, and wealth management.

## Production Direction

- Real KYC/KYB providers.
- Land or title registry integrations where available.
- Bank-grade identity and access management.
- Model monitoring and approval governance.
- Production attestation registry.
- Privacy-preserving audit proofs.
