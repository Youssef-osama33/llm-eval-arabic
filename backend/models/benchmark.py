"""
Benchmark dataset and run ORM models.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column, String, Integer, Float, DateTime,
    ForeignKey, JSON, Text, Boolean, Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class BenchmarkDataset(Base):
    __tablename__ = "benchmark_datasets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    prompt_count = Column(Integer, default=0)
    dialect = Column(String(20), nullable=True)       # null = multi-dialect
    categories = Column(JSON, nullable=True)          # list of category IDs
    source_doi = Column(String(200), nullable=True)
    is_public = Column(Boolean, default=True)
    status = Column(String(20), default="active")     # active | beta | deprecated

    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    prompts = relationship(
        "BenchmarkPrompt", back_populates="dataset", cascade="all, delete-orphan"
    )
    runs = relationship("BenchmarkRun", back_populates="dataset")

    def __repr__(self) -> str:
        return f"<BenchmarkDataset slug={self.slug}>"


class BenchmarkPrompt(Base):
    __tablename__ = "benchmark_prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = Column(
        UUID(as_uuid=True),
        ForeignKey("benchmark_datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    prompt_text = Column(Text, nullable=False)
    reference_answer = Column(Text, nullable=True)
    dialect = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)
    difficulty = Column(String(20), nullable=True)    # easy | medium | hard | expert
    tags = Column(JSON, nullable=True)

    dataset = relationship("BenchmarkDataset", back_populates="prompts")

    __table_args__ = (Index("ix_benchmark_prompts_dataset_id", "dataset_id"),)


class BenchmarkRun(Base):
    __tablename__ = "benchmark_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = Column(
        UUID(as_uuid=True),
        ForeignKey("benchmark_datasets.id"),
        nullable=False,
    )
    model_ids = Column(JSON, nullable=False)          # list of model IDs
    sample_size = Column(Integer, nullable=True)      # null = full dataset
    status = Column(String(20), default="pending")    # pending | running | completed | failed
    results_summary = Column(JSON, nullable=True)     # aggregated scores per model
    error_message = Column(Text, nullable=True)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    dataset = relationship("BenchmarkDataset", back_populates="runs")
