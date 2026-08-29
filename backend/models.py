from typing import Optional

from pydantic import BaseModel, Field


class LeadState(BaseModel):
    """Structured information collected about the customer."""

    name: Optional[str] = None
    configuration: Optional[str] = None
    budget: Optional[str] = None
    purchase_timeline: Optional[str] = None

    interest_level: Optional[str] = None

    site_visit_status: Optional[str] = None
    site_visit_date: Optional[str] = None
    site_visit_time: Optional[str] = None

    follow_up_required: bool = False
    preferred_language: Optional[str] = None

    escalation_required: bool = False
    opted_out: bool = False
    conversation_ended: bool = False


class ChatRequest(BaseModel):
    """Request received from the frontend."""

    session_id: str
    message: str


class ChatResponse(BaseModel):
    """Response returned to the frontend."""

    response: str
    lead_state: LeadState
    analytics: dict


class Session(BaseModel):
    """State maintained for a single conversation."""

    gemini_interaction_id: Optional[str] = None
    lead: LeadState = Field(default_factory=LeadState)