# Production Roadmap

## 24-Hour Hackathon Demo

Product scope:
- one risky Thai condo deposit case;
- Dubai bank funds, USDT holdings, and red P2P/cash-like source;
- Property Shield, Capital Bankability Map, Settlement Route Comparison;
- Closing Passport hash and Evidence Pack JSON export.

User roles:
- buyer;
- banking anchor;
- compliance officer.

Data readiness:
- synthetic documents only;
- deterministic policy rules;
- no real personal data.

Compliance boundary:
- demo risk workflow only;
- no legal guarantee;
- no real KYC/KYB;
- no official title verification.

Integrations:
- local FastAPI;
- Next.js demo UI;
- optional Qdrant/BGE/LLM narrative, deterministic fallback.

Success metrics:
- 3-minute demo is understandable;
- buyer risk is obvious;
- bankable route is clearly better than direct deposit;
- evidence hash is generated live.

Non-promises:
- no production compliance decision;
- no real escrow;
- no real on-chain transaction required.

## 2-Week Pilot

Product scope:
- scenario library for SWIFT, USDT, cash/P2P, and mixed capital;
- verified developer and agent profile stubs;
- RAG trace stub;
- role-based buyer, banker, and compliance views;
- PDF or downloadable evidence export.

User roles:
- buyer;
- bank officer;
- compliance officer;
- verified developer;
- verified agent.

Data readiness:
- expanded synthetic corpus;
- scenario matrix;
- deterministic classification rules;
- traceable synthetic evidence.

Compliance boundary:
- policy simulation;
- escalation categories;
- no regulated decision automation.

Integrations:
- Qdrant collection layout;
- local embedding/reranker services when available;
- LLM-generated explanations behind structured schemas.

Success metrics:
- 3 or more scenarios run end-to-end;
- every scenario has a different route decision;
- evidence export excludes sensitive fields;
- bank user can explain approve/reject/escalate outcome.

Non-promises:
- no live bank data;
- no real wallet analytics;
- no real land registry.

## 6-Week Bank Pilot

Product scope:
- bank intake workflow;
- FET-ready settlement checklist;
- escrow condition workflow;
- audit dashboard;
- pilot metrics dashboard;
- legal review of wording and boundaries.

User roles:
- relationship manager;
- operations officer;
- compliance officer;
- buyer support;
- pilot admin.

Data readiness:
- synthetic plus bank-approved sandbox samples;
- anonymized workflow metrics;
- manually reviewed policy set.

Compliance boundary:
- human-in-the-loop approval;
- model output is advisory;
- final decision remains with bank roles.

Integrations:
- bank document intake sandbox;
- identity provider sandbox;
- wallet analytics sandbox;
- payment rail sandbox or mocked adapter.

Success metrics:
- review time reduction;
- escalation clarity;
- fewer incomplete document packets;
- buyer completion rate;
- bank-captured settlement flow.

Non-promises:
- no autonomous approvals;
- no title guarantee;
- no public claims of regulator endorsement.

## 3-Month Regulated Pilot

Product scope:
- policy versioning;
- approval governance;
- evidence pack retention rules;
- model monitoring;
- incident and dispute workflow;
- privacy review.

User roles:
- bank compliance lead;
- legal reviewer;
- risk officer;
- audit team;
- product owner.

Data readiness:
- controlled pilot data;
- documented consent and retention boundaries;
- test cases for clean, amber, red, and escalation paths.

Compliance boundary:
- bank-approved pilot jurisdiction and scope;
- documented non-replacement of legal/title/KYC providers;
- auditable human approvals.

Integrations:
- KYC/KYB provider sandbox;
- document management;
- audit log;
- attestation registry testnet or private registry.

Success metrics:
- auditability;
- policy adherence;
- false positive/false negative review;
- compliance officer acceptance;
- operational handoff readiness.

Non-promises:
- no open public marketplace;
- no automated final compliance approval;
- no cross-border production rollout.

## 6-Month Multi-Bank Network

Product scope:
- multi-bank anchor model;
- verified participant registry;
- settlement routing across originator and receiving banks;
- developer and agent trust profiles;
- post-purchase finance offers.

User roles:
- originator bank;
- Thai receiving bank;
- escrow provider;
- buyer;
- developer;
- agent;
- platform operator.

Data readiness:
- network participant records;
- sandbox and limited real participant profiles;
- evidence schemas versioned.

Compliance boundary:
- participant-specific permissions;
- bank-specific policy overlays;
- jurisdiction-aware disclosures.

Integrations:
- bank adapters;
- escrow provider adapter;
- wallet risk provider;
- CRM and post-purchase product systems.

Success metrics:
- number of banking anchors;
- verified developer/agent coverage;
- routed settlement volume;
- buyer trust conversion;
- post-purchase product uptake.

Non-promises:
- no universal approval across all banks;
- no guarantee that every property can be routed;
- no public listing marketplace replacement.

## 12-Month Production Platform

Product scope:
- production Bankable Property Network;
- Bankable Property OS operating layer;
- Closing Passport module;
- Property Shield;
- Capital Bankability Map;
- Settlement Routing;
- Escrow and Conditional Release;
- Post-Purchase Financial Layer.

User roles:
- buyers;
- banks;
- compliance teams;
- developers;
- agents;
- auditors;
- platform operations.

Data readiness:
- production data governance;
- retention policies;
- access controls;
- model monitoring and evaluation datasets.

Compliance boundary:
- clear regulated responsibility map;
- legal, bank, and platform role separation;
- privacy-preserving evidence strategy.

Integrations:
- bank production APIs where approved;
- KYC/KYB;
- wallet analytics;
- title or registry integrations where available;
- attestation registry;
- audit and observability stack.

Success metrics:
- verified settlement volume;
- reduced disputed deposits;
- buyer completion and satisfaction;
- bank revenue and captured flow;
- audit outcomes;
- regulator and partner acceptance.

Non-promises:
- no replacement of government registries;
- no guarantee against all fraud;
- no title tokenization claim;
- no unsupported movement of red capital.
