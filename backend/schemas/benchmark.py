"""Pydantic schemas for benchmarks."""

from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field


class BenchmarkDatasetOut(BaseModel):
    id: UUID
    slug: str
    name: str
    description: Optional[str] = None
    prompt_count: int
    dialect: Optional[str] = None
    categories: Optional[List[str]] = None
    source_doi: Optional[str] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BenchmarkRunRequest(BaseModel):
    dataset_slug: str
    model_ids: List[str] = Field(..., min_length=1, max_length=6)
    sample_size: Optional[int] = Field(None, ge=10, le=1000)


class BenchmarkRunOut(BaseModel):
    id: UUID
    dataset_id: UUID
    model_ids: List[str]
    sample_size: Optional[int] = None
    status: str
    results_summary: Optional[Dict] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
