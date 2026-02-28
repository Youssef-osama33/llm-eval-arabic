"""
EvaluatorService — orchestrates parallel async LLM calls via LangChain.
Each model call runs concurrently with a configurable timeout.
"""

import asyncio
import time
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from app.core.config import settings
from app.core.exceptions import ModelNotAvailableError, EvaluationTimeoutError
from app.services.arabic_analyzer import arabic_analyzer

logger = logging.getLogger(__name__)

ARABIC_SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي متخصص في اللغة العربية بجميع لهجاتها ومصطلحاتها التقنية. "
    "قدّم إجابات دقيقة ومفيدة، مع مراعاة السياق اللغوي والثقافي العربي. "
    "التزم باللهجة المطلوبة في إجاباتك.\n\n"
    "You are an AI assistant specialized in Arabic in all its dialects and technical "
    "terminology. Provide accurate, helpful, culturally-aware answers. "
    "Respond in the requested dialect."
)


@dataclass
class SingleModelResult:
    model_id: str
    model_name: str
    provider: str
    response_text: Optional[str]
    latency_ms: int
    token_count: int
    cost_usd: float
    error: Optional[str]
    arabic_metrics: dict


def _build_llm(model_id: str):
    """
    Instantiate the correct LangChain LLM for the given model ID.
    Raises ModelNotAvailableError if the model is unknown or unconfigured.
    """
    try:
        if model_id.startswith("gpt"):
            if not settings.OPENAI_API_KEY:
                raise ModelNotAvailableError(model_id)
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model_id,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.DEFAULT_TEMPERATURE,
                streaming=False,
            )

        elif model_id.startswith("claude"):
            if not settings.ANTHROPIC_API_KEY:
                raise ModelNotAvailableError(model_id)
            from langchain_anthropic import ChatAnthropic
            model_map = {
                "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
                "claude-3-opus": "claude-3-opus-20240229",
            }
            return ChatAnthropic(
                model=model_map.get(model_id, model_id),
                api_key=settings.ANTHROPIC_API_KEY,
                temperature=settings.DEFAULT_TEMPERATURE,
            )

        elif model_id.startswith("gemini"):
            if not settings.GOOGLE_API_KEY:
                raise ModelNotAvailableError(model_id)
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=model_id,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=settings.DEFAULT_TEMPERATURE,
            )

        elif model_id == "llama-3-70b":
            # Via Ollama or Groq — configure GROQ_API_KEY in .env
            from langchain_groq import ChatGroq
            return ChatGroq(model="llama3-70b-8192", temperature=settings.DEFAULT_TEMPERATURE)

        elif model_id == "mistral-large":
            from langchain_mistralai import ChatMistralAI
            return ChatMistralAI(model="mistral-large-latest", temperature=settings.DEFAULT_TEMPERATURE)

        else:
            raise ModelNotAvailableError(model_id)

    except ModelNotAvailableError:
        raise
    except ImportError as e:
        logger.error("LangChain provider not installed for %s: %s", model_id, e)
        raise ModelNotAvailableError(model_id)


MODEL_METADATA: Dict[str, dict] = {
    "gpt-4o":          {"name": "GPT-4o",           "provider": "OpenAI",      "cost_per_1k_out": 0.015},
    "gpt-4-turbo":     {"name": "GPT-4 Turbo",       "provider": "OpenAI",      "cost_per_1k_out": 0.030},
    "gpt-3.5-turbo":   {"name": "GPT-3.5 Turbo",     "provider": "OpenAI",      "cost_per_1k_out": 0.002},
    "claude-3-5-sonnet":{"name": "Claude 3.5 Sonnet","provider": "Anthropic",   "cost_per_1k_out": 0.015},
    "claude-3-opus":   {"name": "Claude 3 Opus",     "provider": "Anthropic",   "cost_per_1k_out": 0.075},
    "gemini-1.5-pro":  {"name": "Gemini 1.5 Pro",    "provider": "Google",      "cost_per_1k_out": 0.007},
    "gemini-1.5-flash":{"name": "Gemini 1.5 Flash",  "provider": "Google",      "cost_per_1k_out": 0.0007},
    "llama-3-70b":     {"name": "LLaMA 3 70B",       "provider": "Meta/Groq",   "cost_per_1k_out": 0.0008},
    "mistral-large":   {"name": "Mistral Large",      "provider": "Mistral AI",  "cost_per_1k_out": 0.006},
    "jais-30b":        {"name": "Jais 30B",           "provider": "G42/MBZUAI", "cost_per_1k_out": 0.002},
}


async def _call_single_model(
    model_id: str,
    prompt: str,
    dialect: str,
    max_tokens: int,
    timeout: int,
) -> SingleModelResult:
    """Call one model and return structured result. Never raises — errors are captured."""
    meta = MODEL_METADATA.get(model_id, {"name": model_id, "provider": "Unknown", "cost_per_1k_out": 0})

    try:
        from langchain_core.messages import HumanMessage, SystemMessage

        llm = _build_llm(model_id)
        messages = [
            SystemMessage(content=ARABIC_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        start = time.monotonic()
        response = await asyncio.wait_for(
            llm.ainvoke(messages, max_tokens=max_tokens),
            timeout=timeout,
        )
        latency_ms = int((time.monotonic() - start) * 1000)

        text = response.content if hasattr(response, "content") else str(response)
        tokens = len(text.split())
        cost = (tokens / 1000) * meta["cost_per_1k_out"]
        metrics = arabic_analyzer.analyze(text, dialect=dialect)

        logger.info("Model %s responded in %dms (%d tokens)", model_id, latency_ms, tokens)

        return SingleModelResult(
            model_id=model_id,
            model_name=meta["name"],
            provider=meta["provider"],
            response_text=text,
            latency_ms=latency_ms,
            token_count=tokens,
            cost_usd=round(cost, 6),
            error=None,
            arabic_metrics=metrics,
        )

    except asyncio.TimeoutError:
        logger.warning("Model %s timed out after %ds", model_id, timeout)
        return SingleModelResult(
            model_id=model_id, model_name=meta["name"], provider=meta["provider"],
            response_text=None, latency_ms=timeout * 1000,
            token_count=0, cost_usd=0.0,
            error=f"Request timed out after {timeout} seconds.",
            arabic_metrics={},
        )
    except Exception as exc:
        logger.exception("Model %s failed: %s", model_id, exc)
        return SingleModelResult(
            model_id=model_id, model_name=meta["name"], provider=meta["provider"],
            response_text=None, latency_ms=-1,
            token_count=0, cost_usd=0.0,
            error=str(exc),
            arabic_metrics={},
        )


async def run_parallel_evaluation(
    prompt: str,
    dialect: str,
    model_ids: List[str],
    max_tokens: int = 1024,
    timeout: int = 120,
) -> List[SingleModelResult]:
    """
    Run all selected models in parallel and return all results.
    Guarantees a result for every model (errors are captured, not raised).
    """
    tasks = [
        _call_single_model(model_id, prompt, dialect, max_tokens, timeout)
        for model_id in model_ids
    ]
    results = await asyncio.gather(*tasks)
    return list(results)
