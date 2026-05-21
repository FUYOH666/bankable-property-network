from typing import Any

from pydantic import BaseModel, Field


class ConsultMessageRequest(BaseModel):
    session_id: str = Field(default="default", max_length=128)
    message: str = Field(min_length=1, max_length=4000)
    channel: str = Field(default="web", max_length=32)


class ConsultMessageResponse(BaseModel):
    data_classification: str
    module: str
    session_id: str
    intent: str = ""
    reply: str
    retrieval_mode: str
    tools_used: list[str]
    citations: list[dict[str, Any]]
    safety_note: str


class ConsultHealthResponse(BaseModel):
    status: str
    module: str
    llm_configured: bool
    active_sessions: int
    knowledge_corpus: dict[str, Any] | None = None
    api_version: str | None = None
