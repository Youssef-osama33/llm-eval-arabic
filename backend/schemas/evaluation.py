"""
Pydantic schemas for evaluation request/response validation.
"""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


# ── Enums ─────────────────────────────────────────────────

VALID_DIALECTS = {"msa", "gulf", "egyptian", "levantine", "maghrebi", "iraqi"}
VALID_CATEGORIES = {
    "dialect_understanding", "technical_terminology", "reasoning",
    "instruction_following", "translation", "creative_writing",
    "code_generation", "culture_heritage",
}
VALID_MODELS = {
    "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo",
    "claude-3-5-sonnet", "claude-3-opus",
    "gemini-1.5-pro", "gemini-1.5-flash",
    "llama-3-70b", "mistral-large", "jais-30b",
}


# ── Request Schemas ───────────────────────────────────────

class EvaluationCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=8000, description="Arabic prompt text")
    dialect: str = Field("msa", description="Target Arabic dialect")
    category: str = Field("dialect_understanding", description="Evaluation category")
    models: List[str] = Field(
        default=["gpt-4o", "claude-3-5-sonnet"],
        min_length=2,
        max_length=6,
        description="Model IDs to compare (2–6 models)",
    )
    reference_answer: Optional[str] = Field(None, max_length=8000)
    max_tokens: int = Field(1024, ge=64, le=4096)

    @field_validator("dialect")
    @classmethod
    def validate_dialect(cls, v: str) -> str:
        if v not in VALID_DIALECTS:
            raise ValueError(f"Dialect must be one of: {sorted(VALID_DIALECTS)}")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {sorted(VALID_CATEGORIES)}")
        return v

    @field_validator("models")
    @classmethod
    def validate_models(cls, v: List[str]) -> List[str]:
        invalid = [m for m in v if m not in VALID_MODELS]
        if invalid:
            raise ValueError(f"Unknown models: {invalid}. Valid: {sorted(VALID_MODELS)}")
        if len(set(v)) != len(v):
            raise ValueError("Duplicate models are not allowed.")
        return v

    model_config = {"json_schema_extra": {
        "example": {
            "prompt": "اشرح الفرق بين الذكاء الاصطناعي والتعلم الآلي",
            "dialect": "msa",
            "category": "technical_terminology",
            "models": ["gpt-4o", "claude-3-5-sonnet", "jais-30b"],
            "max_tokens": 1024,
        }
    }}


# ── Response Schemas ──────────────────────────────────────

class ScoreBreakdown(BaseModel):
    arabic_quality: Optional[float] = None
    accuracy: Optional[float] = None
    dialect_adherence: Optional[float] = None
    technical_precision: Optional[float] = None
    completeness: Optional[float] = None
    cultural_sensitivity: Optional[float] = None
    overall: Optional[float] = None
    reasoning: Optional[str] = None


class ModelResponseOut(BaseModel):
    model_id: str
    model_name: str
    provider: str
    response_text: Optional[str] = None
    latency_ms: Optional[int] = None
    token_count: Optional[int] = None
    cost_usd: Optional[float] = None
    error: Optional[str] = None
    scores: ScoreBreakdown
    arabic_metrics: Optional[Dict] = None

    model_config = {"from_attributes": True}


class EvaluationOut(BaseModel):
    id: UUID
    prompt: str
    dialect: str
    category: str
    status: str
    winner_model_id: Optional[str] = None
    ranking: List[str] = Field(default_factory=list)
    model_responses: List[ModelResponseOut] = Field(default_factory=list)
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class EvaluationListItem(BaseModel):
    id: UUID
    prompt: str
    dialect: str
    category: str
    status: str
    winner_model_id: Optional[str] = None
    model_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedEvaluations(BaseModel):
    items: List[EvaluationListItem]
    total: int
    page: int
    page_size: int
    pages: int
