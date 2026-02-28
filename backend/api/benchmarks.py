"""Benchmark dataset and run endpoints."""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.benchmark import BenchmarkDataset, BenchmarkRun
from app.schemas.benchmark import BenchmarkDatasetOut, BenchmarkRunRequest, BenchmarkRunOut

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])
logger = logging.getLogger(__name__)


@router.get("", response_model=List[BenchmarkDatasetOut], summary="List all benchmark datasets")
async def list_benchmarks(
    status: Optional[str] = Query(None, description="Filter by status: active|beta|deprecated"),
    db: AsyncSession = Depends(get_db),
) -> List[BenchmarkDatasetOut]:
    query = select(BenchmarkDataset).order_by(BenchmarkDataset.prompt_count.desc())
    if status:
        query = query.where(BenchmarkDataset.status == status)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{slug}", response_model=BenchmarkDatasetOut, summary="Get benchmark by slug")
async def get_benchmark(slug: str, db: AsyncSession = Depends(get_db)) -> BenchmarkDatasetOut:
    result = await db.execute(
        select(BenchmarkDataset).where(BenchmarkDataset.slug == slug)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Benchmark '{slug}' not found.")
    return dataset


@router.post("/runs", response_model=BenchmarkRunOut, status_code=202, summary="Start a benchmark run")
async def start_benchmark_run(
    request: BenchmarkRunRequest,
    db: AsyncSession = Depends(get_db),
) -> BenchmarkRunOut:
    # Validate dataset
    result = await db.execute(
        select(BenchmarkDataset).where(BenchmarkDataset.slug == request.dataset_slug)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Benchmark '{request.dataset_slug}' not found.")

    run = BenchmarkRun(
        dataset_id=dataset.id,
        model_ids=request.model_ids,
        sample_size=request.sample_size,
        status="pending",
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)

    logger.info("Benchmark run %s created for dataset %s", run.id, request.dataset_slug)
    return run


@router.get("/runs/{run_id}", response_model=BenchmarkRunOut, summary="Get benchmark run status")
async def get_benchmark_run(run_id: UUID, db: AsyncSession = Depends(get_db)) -> BenchmarkRunOut:
    run = await db.get(BenchmarkRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Benchmark run '{run_id}' not found.")
    return run
