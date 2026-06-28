"""
database/schemas.py
-------------------
Pydantic models define the shape of data coming IN (requests) and going OUT (responses).
They are separate from SQLAlchemy models:
  - SQLAlchemy models = database structure
  - Pydantic schemas  = API contract (what the frontend sends/receives)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Request ────────────────────────────────────────────────────────────────────

class QuoteSearchRequest(BaseModel):
    quote: str = Field(..., min_length=5, max_length=1000, description="The quote to research")

    model_config = {
        "json_schema_extra": {
            "example": {"quote": "Blood, sweat, and tears"}
        }
    }


# ── Response pieces ────────────────────────────────────────────────────────────

class SourceOut(BaseModel):
    id: int
    platform: str
    title: Optional[str]
    url: Optional[str]
    snippet: Optional[str]
    mentioned_date: Optional[str]
    speaker_mentioned: Optional[str]
    relevance: Optional[float]

    model_config = {"from_attributes": True}


class QuoteOut(BaseModel):
    id: int
    input_text: str
    original_phrasing: Optional[str]
    speaker: Optional[str]
    earliest_date: Optional[str]
    confidence_score: Optional[float]
    reasoning: Optional[str]
    is_resolved: bool
    sources: list[SourceOut] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchResponse(BaseModel):
    quote: QuoteOut
    cache_hit: bool
    sources_found: int
    duration_ms: Optional[int]
