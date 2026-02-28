"""
SQLAlchemy ORM models for evaluations and model responses.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Column, String, Float, Integer, Text, DateTime,
    ForeignKey, JSON, Enum as SAEnum, Boolean, Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Evaluation(Base):
    """
    A single evaluation run — one prompt compared across N models.
    """
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(Text, nullable=False)
    dialect = Column(String(20), nullable=False, default="msa")
    category = Column(String(50), nullable=False, default="general")
    reference_answer = Column(Text, nullable=True)
    max_tokens = Column(Integer, default=1024)
    status = Column(
        SAEnum("pending", "running", "completed", "failed", name="eval_status"),
        default="pending",
        nullable=False,
    )
    error_message = Column(Text, nullable=True)
    winner_model_id = Column(String(50), nullable=True)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    model_responses = relationship(
        "ModelResponse", back_populates="evaluation", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_evaluations_created_at", "created_at"),
        Index("ix_evaluations_dialect", "dialect"),
        Index("ix_evaluations_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Evaluation id={self.id} dialect={self.dialect} status={self.status}>"


class ModelResponse(Base):
    """
    A single model's response within an evaluation, with scores.
    """
    __tablename__ = "model_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("evaluations.id", ondelete="CASCADE"),
        nullable=False,
    )
    model_id = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)

    response_text = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)
    error = Column(Text, nullable=True)

    # Scores from LLM-as-Judge (0–10 each)
    score_arabic_quality = Column(Float, nullable=True)
    score_accuracy = Column(Float, nullable=True)
    score_dialect_adherence = Column(Float, nullable=True)
    score_technical_precision = Column(Float, nullable=True)
    score_completeness = Column(Float, nullable=True)
    score_cultural_sensitivity = Column(Float, nullable=True)
    score_overall = Column(Float, nullable=True)
    score_reasoning = Column(Text, nullable=True)

    # Arabic NLP metrics
    arabic_metrics = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    evaluation = relationship("Evaluation", back_populates="model_responses")

    __table_args__ = (
        Index("ix_model_responses_evaluation_id", "evaluation_id"),
        Index("ix_model_responses_model_id", "model_id"),
    )

    @property
    def scores_dict(self) -> dict:
        return {
            "arabic_quality": self.score_arabic_quality,
            "accuracy": self.score_accuracy,
            "dialect_adherence": self.score_dialect_adherence,
            "technical_precision": self.score_technical_precision,
            "completeness": self.score_completeness,
            "cultural_sensitivity": self.score_cultural_sensitivity,
            "overall": self.score_overall,
        }

    def __repr__(self) -> str:
        return f"<ModelResponse model={self.model_id} overall={self.score_overall}>"
