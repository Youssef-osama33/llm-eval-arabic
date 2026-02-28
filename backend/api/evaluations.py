"""
Evaluation API routes.
POST /evaluations/run  — create and run an evaluation
GET  /evaluations      — list with pagination
GET  /evaluations/{id} — retrieve single evaluation
"""

import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.exceptions import EvaluationNotFoundError
from app.models.evaluation import Evaluation, ModelResponse
from app.schemas.evaluation import (
    EvaluationCreateRequest,
    EvaluationOut,
    EvaluationListItem,
    PaginatedEvaluations,
    ModelResponseOut,
    ScoreBreakdown,
)
from app.services.evaluator import run_parallel_evaluation
from app.services.scorer import score_all_responses

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])
logger = logging.getLogger(__name__)


async def _run_evaluation_pipeline(
    evaluation_id: UUID,
    request: EvaluationCreateRequest,
    db: AsyncSession,
) -> None:
    """
    Background task: run models, score responses, persist to DB.
    """
    # Fetch fresh session for background task
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as bg_db:
        try:
            # Mark as running
            eval_obj = await bg_db.get(Evaluation, evaluation_id)
            if not eval_obj:
                return
            eval_obj.status = "running"
            await bg_db.commit()

            # Run all models in parallel
            results = await run_parallel_evaluation(
                prompt=request.prompt,
                dialect=request.dialect,
                model_ids=request.models,
                max_tokens=request.max_tokens,
            )

            # Score all responses concurrently
            all_scores = await score_all_responses(
                results=results,
                prompt=request.prompt,
                dialect=request.dialect,
                category=request.category,
                reference_answer=request.reference_answer,
            )

            # Determine winner (highest overall score among non-error responses)
            winner_id: Optional[str] = None
            best_score: float = -1.0
            for result, scores in zip(results, all_scores):
                overall = scores.get("overall") or 0.0
                if not result.error and overall > best_score:
                    best_score = overall
                    winner_id = result.model_id

            # Persist model responses
            for result, scores in zip(results, all_scores):
                mr = ModelResponse(
                    evaluation_id=evaluation_id,
                    model_id=result.model_id,
                    model_name=result.model_name,
                    provider=result.provider,
                    response_text=result.response_text,
                    latency_ms=result.latency_ms,
                    token_count=result.token_count,
                    cost_usd=result.cost_usd,
                    error=result.error,
                    score_arabic_quality=scores.get("arabic_quality"),
                    score_accuracy=scores.get("accuracy"),
                    score_dialect_adherence=scores.get("dialect_adherence"),
                    score_technical_precision=scores.get("technical_precision"),
                    score_completeness=scores.get("completeness"),
                    score_cultural_sensitivity=scores.get("cultural_sensitivity"),
                    score_overall=scores.get("overall"),
                    score_reasoning=scores.get("reasoning"),
                    arabic_metrics=result.arabic_metrics,
                )
                bg_db.add(mr)

            # Update evaluation
            eval_obj = await bg_db.get(Evaluation, evaluation_id)
            eval_obj.status = "completed"
            eval_obj.winner_model_id = winner_id
            eval_obj.completed_at = datetime.now(timezone.utc)
            await bg_db.commit()

            logger.info("Evaluation %s completed. Winner: %s", evaluation_id, winner_id)

        except Exception as exc:
            logger.exception("Evaluation %s failed: %s", evaluation_id, exc)
            async with AsyncSessionLocal() as err_db:
                eval_obj = await err_db.get(Evaluation, evaluation_id)
                if eval_obj:
                    eval_obj.status = "failed"
                    eval_obj.error_message = str(exc)
                    await err_db.commit()


@router.post(
    "/run",
    response_model=EvaluationOut,
    status_code=202,
    summary="Create and run an evaluation",
    description="Submit an Arabic prompt to be evaluated across multiple LLMs. "
                "The evaluation runs asynchronously — poll GET /evaluations/{id} for results.",
)
async def run_evaluation(
    request: EvaluationCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> EvaluationOut:
    # Create evaluation record
    evaluation = Evaluation(
        prompt=request.prompt,
        dialect=request.dialect,
        category=request.category,
        reference_answer=request.reference_answer,
        max_tokens=request.max_tokens,
        status="pending",
    )
    db.add(evaluation)
    await db.commit()
    await db.refresh(evaluation)

    # Schedule background pipeline
    background_tasks.add_task(
        _run_evaluation_pipeline,
        evaluation.id,
        request,
        db,
    )

    logger.info(
        "Evaluation %s created (%d models, dialect=%s)",
        evaluation.id, len(request.models), request.dialect,
    )

    return _evaluation_to_out(evaluation)


@router.get(
    "",
    response_model=PaginatedEvaluations,
    summary="List evaluations with pagination",
)
async def list_evaluations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    dialect: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> PaginatedEvaluations:
    query = select(Evaluation).order_by(Evaluation.created_at.desc())

    if dialect:
        query = query.where(Evaluation.dialect == dialect)
    if status:
        query = query.where(Evaluation.status == status)

    # Total count
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    # Paginated items
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    evaluations = result.scalars().all()

    items = []
    for ev in evaluations:
        count_resp = await db.execute(
            select(func.count(ModelResponse.id)).where(ModelResponse.evaluation_id == ev.id)
        )
        model_count = count_resp.scalar_one()
        items.append(EvaluationListItem(
            id=ev.id,
            prompt=ev.prompt[:120] + ("..." if len(ev.prompt) > 120 else ""),
            dialect=ev.dialect,
            category=ev.category,
            status=ev.status,
            winner_model_id=ev.winner_model_id,
            model_count=model_count,
            created_at=ev.created_at,
        ))

    return PaginatedEvaluations(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size,
    )


@router.get(
    "/{evaluation_id}",
    response_model=EvaluationOut,
    summary="Get a single evaluation with full results",
)
async def get_evaluation(
    evaluation_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> EvaluationOut:
    result = await db.execute(
        select(Evaluation).where(Evaluation.id == evaluation_id)
    )
    evaluation = result.scalar_one_or_none()
    if not evaluation:
        raise EvaluationNotFoundError(str(evaluation_id))

    # Load model responses
    resp_result = await db.execute(
        select(ModelResponse)
        .where(ModelResponse.evaluation_id == evaluation_id)
        .order_by(ModelResponse.score_overall.desc().nulls_last())
    )
    responses = resp_result.scalars().all()
    evaluation.model_responses = responses

    return _evaluation_to_out(evaluation, include_responses=True)


# ── Helpers ────────────────────────────────────────────────

def _evaluation_to_out(
    evaluation: Evaluation,
    include_responses: bool = False,
) -> EvaluationOut:
    responses_out = []
    if include_responses and evaluation.model_responses:
        for mr in evaluation.model_responses:
            responses_out.append(ModelResponseOut(
                model_id=mr.model_id,
                model_name=mr.model_name,
                provider=mr.provider,
                response_text=mr.response_text,
                latency_ms=mr.latency_ms,
                token_count=mr.token_count,
                cost_usd=mr.cost_usd,
                error=mr.error,
                scores=ScoreBreakdown(
                    arabic_quality=mr.score_arabic_quality,
                    accuracy=mr.score_accuracy,
                    dialect_adherence=mr.score_dialect_adherence,
                    technical_precision=mr.score_technical_precision,
                    completeness=mr.score_completeness,
                    cultural_sensitivity=mr.score_cultural_sensitivity,
                    overall=mr.score_overall,
                    reasoning=mr.score_reasoning,
                ),
                arabic_metrics=mr.arabic_metrics,
            ))

    ranking = [
        r.model_id for r in evaluation.model_responses
        if r.score_overall is not None
    ] if evaluation.model_responses else []

    return EvaluationOut(
        id=evaluation.id,
        prompt=evaluation.prompt,
        dialect=evaluation.dialect,
        category=evaluation.category,
        status=evaluation.status,
        winner_model_id=evaluation.winner_model_id,
        ranking=ranking,
        model_responses=responses_out,
        created_at=evaluation.created_at,
        completed_at=evaluation.completed_at,
    )
