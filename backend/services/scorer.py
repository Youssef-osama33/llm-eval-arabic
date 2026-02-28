"""
ScorerService — LLM-as-Judge scoring.
Uses GPT-4o (or configured judge model) to evaluate each model response
across 6 linguistic and quality dimensions.
"""

import json
import logging
import asyncio
from typing import Optional

from app.core.config import settings
from app.core.exceptions import ScoringError
from app.services.evaluator import SingleModelResult

logger = logging.getLogger(__name__)

SCORE_DIMENSIONS = [
    "arabic_quality",       # grammar, fluency, naturalness
    "accuracy",             # factual correctness
    "dialect_adherence",    # match to requested dialect
    "technical_precision",  # domain terminology correctness
    "completeness",         # how thoroughly it answers
    "cultural_sensitivity", # cultural appropriateness
]

JUDGE_SYSTEM_PROMPT = """أنت محكّم خبير في تقييم مخرجات نماذج اللغة العربية.

You are an expert judge evaluating Arabic language model outputs.
Score each response on these 6 dimensions (0.0–10.0 each):

1. arabic_quality      — Grammar, fluency, naturalness of Arabic
2. accuracy            — Factual correctness and relevance to the prompt
3. dialect_adherence   — How well it matches the requested Arabic dialect
4. technical_precision — Correct use of technical or domain-specific terminology
5. completeness        — How thoroughly and completely it addresses the prompt
6. cultural_sensitivity — Cultural appropriateness for an Arab audience

Scoring scale:
  9.5–10.0 → Exceptional / Native-level
  8.0–9.4  → Strong / Professional quality
  6.0–7.9  → Acceptable / Minor issues
  4.0–5.9  → Weak / Significant problems
  0.0–3.9  → Poor / Fails the dimension

CRITICAL: Respond ONLY with valid JSON — no markdown fences, no preamble:
{
  "arabic_quality": <float>,
  "accuracy": <float>,
  "dialect_adherence": <float>,
  "technical_precision": <float>,
  "completeness": <float>,
  "cultural_sensitivity": <float>,
  "overall": <weighted_average_float>,
  "reasoning": "<one sentence Arabic or English explanation>"
}"""

SCORE_WEIGHTS = {
    "arabic_quality": 0.25,
    "accuracy": 0.25,
    "dialect_adherence": 0.20,
    "technical_precision": 0.15,
    "completeness": 0.10,
    "cultural_sensitivity": 0.05,
}


def _weighted_overall(scores: dict) -> float:
    total = sum(
        scores.get(dim, 0.0) * weight
        for dim, weight in SCORE_WEIGHTS.items()
    )
    return round(total, 2)


def _parse_score_json(raw: str) -> dict:
    """
    Parse the judge's JSON response. Strips markdown fences if present.
    Returns a safe dict with None values on parse failure.
    """
    cleaned = raw.strip()
    # Strip potential ```json ... ``` fences
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(
            line for line in lines
            if not line.strip().startswith("```")
        )
    try:
        data = json.loads(cleaned)
        # Clamp all scores to 0–10
        for dim in SCORE_DIMENSIONS:
            if dim in data:
                data[dim] = max(0.0, min(10.0, float(data[dim])))
        # Recompute overall from weighted formula if not provided or invalid
        if "overall" not in data or not isinstance(data["overall"], (int, float)):
            data["overall"] = _weighted_overall(data)
        else:
            data["overall"] = max(0.0, min(10.0, float(data["overall"])))
        return data
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Failed to parse judge JSON: %s | raw: %.200s", exc, raw)
        return {dim: None for dim in SCORE_DIMENSIONS} | {"overall": None, "reasoning": "Scoring parse error."}


async def score_single_response(
    prompt: str,
    response_text: str,
    dialect: str,
    category: str,
    reference_answer: Optional[str],
    retries: int = 2,
) -> dict:
    """
    Call the judge model to score one response.
    Retries up to `retries` times on failure.
    """
    if not settings.OPENAI_API_KEY:
        logger.warning("No OPENAI_API_KEY configured — returning null scores.")
        return {dim: None for dim in SCORE_DIMENSIONS} | {"overall": None, "reasoning": "Judge model not configured."}

    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage

    judge = ChatOpenAI(
        model=settings.JUDGE_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=settings.JUDGE_TEMPERATURE,
    )

    ref_block = f"\nReference Answer:\n{reference_answer}" if reference_answer else ""
    user_content = (
        f"Dialect requested: {dialect}\n"
        f"Category: {category}\n\n"
        f"Prompt:\n{prompt}\n\n"
        f"Model Response:\n{response_text}"
        f"{ref_block}\n\n"
        "Score this response. Return only the JSON object."
    )

    for attempt in range(retries + 1):
        try:
            messages = [
                SystemMessage(content=JUDGE_SYSTEM_PROMPT),
                HumanMessage(content=user_content),
            ]
            result = await judge.ainvoke(messages, max_tokens=512)
            raw = result.content if hasattr(result, "content") else str(result)
            scores = _parse_score_json(raw)
            logger.debug("Scored response for model (attempt %d)", attempt + 1)
            return scores
        except Exception as exc:
            logger.warning("Judge attempt %d/%d failed: %s", attempt + 1, retries + 1, exc)
            if attempt < retries:
                await asyncio.sleep(1.5 ** attempt)
            else:
                logger.error("All judge attempts exhausted for response.")
                return {dim: None for dim in SCORE_DIMENSIONS} | {
                    "overall": None,
                    "reasoning": f"Scoring failed after {retries + 1} attempts: {exc}",
                }


async def score_all_responses(
    results: list[SingleModelResult],
    prompt: str,
    dialect: str,
    category: str,
    reference_answer: Optional[str],
) -> list[dict]:
    """
    Score all model responses concurrently (only successful responses).
    Returns a list of score dicts aligned with `results`.
    """
    tasks = []
    for r in results:
        if r.response_text and not r.error:
            tasks.append(
                score_single_response(
                    prompt=prompt,
                    response_text=r.response_text,
                    dialect=dialect,
                    category=category,
                    reference_answer=reference_answer,
                )
            )
        else:
            # Failed responses get null scores immediately
            tasks.append(
                asyncio.coroutine(lambda: {dim: None for dim in SCORE_DIMENSIONS} | {
                    "overall": None, "reasoning": "Model returned an error."
                })()
            )

    all_scores = await asyncio.gather(*tasks, return_exceptions=True)
    out = []
    for score in all_scores:
        if isinstance(score, Exception):
            logger.error("Score gather exception: %s", score)
            out.append({dim: None for dim in SCORE_DIMENSIONS} | {"overall": None, "reasoning": str(score)})
        else:
            out.append(score)
    return out
