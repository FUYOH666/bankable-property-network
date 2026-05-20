import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.demo_case import ANCHOR_CASE
from app.logging_config import configure_logging
from app.schemas.demo import (
    ClosingPassportResponse,
    DeveloperKnowledgeHubResponse,
    GuidedSimulationResponse,
    PostClosingYieldPlanResponse,
    SupplierContrastResponse,
)
from app.services.closing_passport_demo import build_closing_passport_demo
from app.services.data_loader import DataLoadError
from app.services.developer_knowledge import build_developer_knowledge_hub
from app.services.rag import ingest_synthetic_documents, rag_health, run_scenario_with_rag
from app.services.scenarios import get_scenario_detail, list_scenarios, run_scenario
from app.services.supplier_contrast_demo import build_supplier_contrast_demo
from app.services.yield_plan import build_post_closing_yield_plan


logger = logging.getLogger(__name__)


def _cors_origins() -> list[str]:
    default_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://scanovich.ai",
        "https://www.scanovich.ai",
    ]
    configured = get_settings().bankable_cors_origins
    if not configured.strip():
        return default_origins
    return [origin.strip() for origin in configured.split(",") if origin.strip()]


def _data_unavailable_http() -> HTTPException:
    return HTTPException(status_code=503, detail="Synthetic demo data unavailable")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.bankable_log_level)
    logger.info("Bankable Property OS API starting version=%s", settings.bankable_api_version)
    yield


app = FastAPI(
    title="Bankable Property OS API",
    description="Closing Passport demo API for bankable Thai property settlement.",
    version=get_settings().bankable_api_version,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "bankable-property-os-api"}


@app.get("/api/demo/closing-passport", response_model=ClosingPassportResponse)
def get_closing_passport_demo() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/closing-passport")
    try:
        return build_closing_passport_demo()
    except DataLoadError as exc:
        logger.error("Closing passport demo failed: %s", exc)
        raise _data_unavailable_http() from exc


@app.get("/api/demo/guided-simulation", response_model=GuidedSimulationResponse)
def get_guided_simulation_demo() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/guided-simulation")
    try:
        demo = build_closing_passport_demo()
    except DataLoadError as exc:
        logger.error("Guided simulation demo failed: %s", exc)
        raise _data_unavailable_http() from exc

    closing_passport = demo["closing_passport"]

    synthetic_artifacts = {
        "agent_message": {
            "data_classification": "synthetic_demo_data",
            "from": "Property agent",
            "message": "Please send the booking deposit today to secure the unit. The receiving company is SRL Holding 2026 Co., Ltd.",
        },
        "payment_instruction": {
            "data_classification": "synthetic_demo_data",
            "expected_payee": ANCHOR_CASE["expected_payee"],
            "instruction_payee": ANCHOR_CASE["payment_instruction_payee"],
            "deadline_hours": ANCHOR_CASE["deposit_deadline_hours"],
        },
        "compliance_memo": {
            "data_classification": "synthetic_demo_data",
            "decision": "approve_bankable_escrow_route",
            "memo": "Direct deposit should pause until payee authority is verified. Escrow route may proceed with corrected instructions.",
        },
        "escrow_draft": {
            "data_classification": "synthetic_demo_data",
            "release_condition": "Release only after verified payee authority and compliance approval.",
        },
    }

    steps = [
        {
            "id": "buyer_pressure",
            "actor": "buyer",
            "title": "Buyer receives urgent deposit pressure",
            "detail": synthetic_artifacts["agent_message"]["message"],
        },
        {
            "id": "document_review",
            "actor": "system",
            "title": "Payment instruction reviewed",
            "detail": "Expected developer and instructed payee do not match.",
        },
        {
            "id": "risk_flags",
            "actor": "property_shield",
            "title": "Property Shield flags the case",
            "detail": ", ".join(demo["property_shield"]["flags"]),
        },
        {
            "id": "bank_counter_offer",
            "actor": "bank",
            "title": "Bank proposes safer settlement",
            "detail": demo["bank_counter_offer"]["offer"],
        },
        {
            "id": "compliance_approval",
            "actor": "compliance",
            "title": "Compliance approves controlled route",
            "detail": synthetic_artifacts["compliance_memo"]["memo"],
        },
        {
            "id": "closing_passport",
            "actor": "system",
            "title": "Closing Passport generated",
            "detail": f"Evidence hash {closing_passport['evidence_pack_hash']} created without sensitive data on-chain.",
        },
    ]

    return {
        "steps": steps,
        "synthetic_artifacts": synthetic_artifacts,
        "evidence_preview": {
            "included": ["case_id", "risk_report", "capital_map", "recommended_route", "approver_role"],
            "excluded_sensitive_fields": ["passport_number", "email", "phone", "address", "full_name"],
            "privacy_note": "Evidence preview uses extracted facts and status metadata only.",
        },
        "closing_passport": closing_passport,
        "infrastructure_context": demo["infrastructure_context"],
    }


@app.get("/api/demo/developer-knowledge-hub", response_model=DeveloperKnowledgeHubResponse)
def get_developer_knowledge_hub_demo() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/developer-knowledge-hub")
    try:
        return build_developer_knowledge_hub(ANCHOR_CASE)
    except DataLoadError as exc:
        logger.error("Developer knowledge hub failed: %s", exc)
        raise _data_unavailable_http() from exc


@app.get("/api/demo/supplier-contrast", response_model=SupplierContrastResponse)
def get_supplier_contrast_demo() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/supplier-contrast")
    try:
        return build_supplier_contrast_demo()
    except (DataLoadError, ValueError) as exc:
        logger.error("Supplier contrast demo failed: %s", exc)
        raise _data_unavailable_http() from exc


@app.get("/api/demo/post-closing-yield-plan", response_model=PostClosingYieldPlanResponse)
def get_post_closing_yield_plan_demo() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/post-closing-yield-plan")
    try:
        return build_post_closing_yield_plan(ANCHOR_CASE)
    except DataLoadError as exc:
        logger.error("Post-closing yield plan failed: %s", exc)
        raise _data_unavailable_http() from exc


@app.get("/api/demo/evidence-pack")
def get_evidence_pack_export() -> dict[str, object]:
    logger.info("Demo endpoint hit path=/api/demo/evidence-pack")
    try:
        demo = build_closing_passport_demo()
    except DataLoadError as exc:
        logger.error("Evidence pack export failed: %s", exc)
        raise _data_unavailable_http() from exc

    closing_passport = demo["closing_passport"]

    return {
        "data_classification": "synthetic_demo_data",
        "export_type": "closing_passport_evidence_pack",
        "case_id": closing_passport["case_id"],
        "evidence_pack_hash": closing_passport["evidence_pack_hash"],
        "evidence": closing_passport["evidence"],
        "attestation": closing_passport["attestation"],
        "privacy_note": "This export contains extracted facts and status metadata only. It excludes raw bank statements, passports, contracts, and personal data.",
    }


@app.get("/api/scenarios")
def get_scenarios() -> dict[str, object]:
    try:
        return {"data_classification": "synthetic_demo_data", "scenarios": list_scenarios()}
    except DataLoadError as exc:
        logger.error("Scenario list failed: %s", exc)
        raise _data_unavailable_http() from exc


@app.get("/api/scenarios/{scenario_id}/run")
def run_synthetic_scenario(scenario_id: str) -> dict[str, object]:
    try:
        result = run_scenario(scenario_id)
    except DataLoadError as exc:
        logger.error("Scenario run failed: %s", exc)
        raise _data_unavailable_http() from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return result


@app.get("/api/scenarios/{scenario_id}/rag-run")
def run_synthetic_scenario_with_rag(scenario_id: str, mode: str = "auto") -> dict[str, object]:
    try:
        result = run_scenario_with_rag(scenario_id, mode=mode)
    except DataLoadError as exc:
        logger.error("Scenario RAG run failed: %s", exc)
        raise _data_unavailable_http() from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return result


@app.get("/api/scenarios/{scenario_id}")
def get_synthetic_scenario(scenario_id: str) -> dict[str, object]:
    try:
        detail = get_scenario_detail(scenario_id)
    except DataLoadError as exc:
        logger.error("Scenario detail failed: %s", exc)
        raise _data_unavailable_http() from exc
    if detail is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return detail


@app.get("/api/rag/health")
def get_rag_health() -> dict[str, object]:
    return rag_health()


@app.post("/api/rag/ingest")
def post_rag_ingest(dry_run: bool = False) -> dict[str, object]:
    return ingest_synthetic_documents(dry_run=dry_run)
