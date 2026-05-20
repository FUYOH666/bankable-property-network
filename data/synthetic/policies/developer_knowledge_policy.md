# Developer Knowledge Policy

Data classification: synthetic demo data.

Policy snippets for the Verified Developer Knowledge Layer in Bankable Property Network.

## Source Of Truth

The developer ERP or authorized feed is the canonical source for:

- available inventory and pricing;
- authorized payee legal entities;
- booking deposit percentages and installment schedules;
- foreign buyer settlement notes;
- project-specific payment instructions.

Agencies and agents must not invent, override, or distort these facts to accelerate commission capture.

## Publication Rules

- Only developer-authorized staff may publish or refresh the knowledge feed.
- Feed freshness must be visible (last updated timestamp).
- Stale feeds beyond the configured window require human review before agent distribution.
- Payment instructions from agents that differ from the developer feed trigger escalation.

## Agent Consumption Model

Verified agencies and platform-connected agents receive read-only access to the developer knowledge hub.

They may:

- answer buyer questions from retrieved developer corpus;
- route handoff to human sales when out of domain;
- cite feed version in compliance and settlement evidence.

They may not:

- substitute unauthorized payee entities;
- promise terms not present in the developer feed;
- bypass the hub with ad hoc payment instructions.

## Relationship To Settlement

Developer knowledge is upstream of Property Shield and Closing Passport.

When payment instruction payee differs from authorized payees in the developer feed, the system should flag mismatch and block direct deposit until corrected.

## Channel Distribution Roadmap

Developer-verified knowledge may be distributed through controlled channels:

- WhatsApp;
- Telegram;
- Email;
- Web chat;
- Voice assistant with TTS (future).

Channels consume the same RAG corpus: embeddings, Qdrant retrieval, reranker, schema-bound LLM responses.

## Boundaries

The Developer Knowledge Layer does not move money, perform KYC, or replace developer CRM systems. It provides verified facts for agents and connects to bank-grade settlement infrastructure downstream.
