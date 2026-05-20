from typing import Any

from pydantic import BaseModel, Field


class InfrastructureContext(BaseModel):
    failure_mode: str
    root_cause: str
    narrative_role: str
    primary_customer: str


class RouteItem(BaseModel):
    id: str
    label: str
    recommended: bool
    risk: str
    conditions: list[str]


class BankCounterOffer(BaseModel):
    product: str
    offer: str
    buyer_value: str
    bank_value: str


class ClosingPassportAttestation(BaseModel):
    buyer_bankability_checked: bool
    developer_risk_reviewed: bool
    settlement_route_approved: bool
    escrow_conditions_generated: bool
    evidence_pack_hash: str
    timestamp: str
    approver_role: str


class ClosingPassportPayload(BaseModel):
    case_id: str
    evidence_pack_hash: str
    evidence: dict[str, Any]
    attestation: ClosingPassportAttestation


class ClosingPassportResponse(BaseModel):
    case: dict[str, Any]
    property_shield: dict[str, Any]
    capital_bankability_map: dict[str, dict[str, Any]]
    routes: list[RouteItem]
    recommended_route: RouteItem
    bank_counter_offer: BankCounterOffer
    closing_passport: ClosingPassportPayload
    infrastructure_context: InfrastructureContext


class SimulationStep(BaseModel):
    id: str
    actor: str
    title: str
    detail: str


class EvidencePreview(BaseModel):
    included: list[str]
    excluded_sensitive_fields: list[str]
    privacy_note: str


class GuidedSimulationResponse(BaseModel):
    steps: list[SimulationStep]
    synthetic_artifacts: dict[str, Any]
    evidence_preview: EvidencePreview
    closing_passport: ClosingPassportPayload
    infrastructure_context: InfrastructureContext


class KnowledgeGap(BaseModel):
    agent_claimed_payee: str
    developer_authorized_payee: str
    status: str
    note: str


class ChannelRoadmapItem(BaseModel):
    id: str
    label: str
    status: str


class DeveloperKnowledgeHubResponse(BaseModel):
    data_classification: str
    module: str
    vision_note: str
    developer: str
    project: str
    source_of_truth: str
    feed_snapshot: dict[str, Any]
    knowledge_vs_agent_gap: KnowledgeGap
    consumption_model: str
    channel_roadmap: list[ChannelRoadmapItem]
    ai_stack: dict[str, str]
    prior_art: dict[str, str]
    downstream_link: str
    pitch_line: str


class PostClosingYieldPlanResponse(BaseModel):
    data_classification: str
    module: str
    vision_note: str
    case_id: str
    property_summary: dict[str, Any]
    after_purchase: dict[str, Any]
    legal_rental_mode: dict[str, Any]
    verified_managers: list[dict[str, Any]]
    recommended_manager: dict[str, Any]
    bank_value: dict[str, str]


class SupplierContrastTrack(BaseModel):
    track: str
    developer: str
    project: str
    scenario_id: str
    headline: str
    risk_summary: str
    bank_action: str
    closing_passport_status: str
    supply_risk_signals: list[str]


class SupplierContrastResponse(BaseModel):
    data_classification: str
    module: str
    pitch_line: str
    off_platform: dict[str, Any]
    on_network: dict[str, Any]
