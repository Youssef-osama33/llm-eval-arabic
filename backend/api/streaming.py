"""
WebSocket endpoint for real-time streaming evaluation.
Clients receive tokens as they arrive from each model.
"""

import asyncio
import json
import logging
import uuid
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.config import settings
from app.services.arabic_analyzer import arabic_analyzer

router = APIRouter(tags=["Streaming"])
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي متخصص في اللغة العربية. "
    "قدّم إجابات دقيقة ومفيدة مع مراعاة السياق الثقافي العربي."
)


async def _stream_model(
    ws: WebSocket,
    model_id: str,
    prompt: str,
    dialect: str,
    max_tokens: int,
) -> str:
    """Stream one model's response; send token events over ws. Returns full text."""
    import time
    from langchain_core.messages import HumanMessage, SystemMessage

    full_tokens: List[str] = []

    try:
        # Build LLM with streaming
        if model_id.startswith("gpt"):
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=model_id, api_key=settings.OPENAI_API_KEY,
                             temperature=0.3, streaming=True)
        elif model_id.startswith("claude"):
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            from langchain_anthropic import ChatAnthropic
            model_map = {"claude-3-5-sonnet": "claude-3-5-sonnet-20241022"}
            llm = ChatAnthropic(model=model_map.get(model_id, model_id),
                                api_key=settings.ANTHROPIC_API_KEY, temperature=0.3)
        elif model_id.startswith("gemini"):
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not configured")
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model=model_id,
                                         google_api_key=settings.GOOGLE_API_KEY,
                                         temperature=0.3)
        else:
            raise ValueError(f"Model '{model_id}' does not support streaming")

        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
        start = time.monotonic()

        await ws.send_json({"type": "stream_start", "model_id": model_id})

        async for chunk in llm.astream(messages, max_tokens=max_tokens):
            token = chunk.content if hasattr(chunk, "content") else str(chunk)
            if token:
                full_tokens.append(token)
                await ws.send_json({"type": "token", "model_id": model_id, "token": token})

        latency_ms = int((time.monotonic() - start) * 1000)
        full_text = "".join(full_tokens)
        metrics = arabic_analyzer.analyze(full_text, dialect=dialect)

        await ws.send_json({
            "type": "stream_end",
            "model_id": model_id,
            "latency_ms": latency_ms,
            "token_count": len(full_text.split()),
            "arabic_metrics": metrics,
        })
        return full_text

    except Exception as exc:
        logger.error("Streaming error for %s: %s", model_id, exc)
        await ws.send_json({"type": "stream_error", "model_id": model_id, "error": str(exc)})
        return ""


@router.websocket("/ws/evaluate")
async def websocket_evaluate(ws: WebSocket) -> None:
    """
    WebSocket endpoint for real-time streaming evaluation.

    Protocol (client → server):
    ```json
    {
      "prompt": "...",
      "dialect": "msa",
      "models": ["gpt-4o", "claude-3-5-sonnet"],
      "max_tokens": 1024
    }
    ```

    Protocol (server → client):
    - {"type": "evaluation_start", "evaluation_id": "...", "models": [...]}
    - {"type": "stream_start", "model_id": "..."}
    - {"type": "token", "model_id": "...", "token": "..."}  (many)
    - {"type": "stream_end", "model_id": "...", "latency_ms": N, ...}
    - {"type": "evaluation_complete", "evaluation_id": "..."}
    """
    await ws.accept()
    evaluation_id = str(uuid.uuid4())

    try:
        data = await asyncio.wait_for(ws.receive_json(), timeout=30)
        prompt = data.get("prompt", "").strip()
        dialect = data.get("dialect", "msa")
        model_ids: List[str] = data.get("models", ["gpt-4o"])
        max_tokens: int = min(int(data.get("max_tokens", 1024)), 4096)

        if not prompt:
            await ws.send_json({"type": "error", "message": "Prompt is required."})
            return

        await ws.send_json({
            "type": "evaluation_start",
            "evaluation_id": evaluation_id,
            "models": model_ids,
        })

        # Stream all models concurrently
        tasks = [
            _stream_model(ws, mid, prompt, dialect, max_tokens)
            for mid in model_ids
        ]
        await asyncio.gather(*tasks)

        await ws.send_json({"type": "evaluation_complete", "evaluation_id": evaluation_id})

    except WebSocketDisconnect:
        logger.info("Client disconnected from WS evaluation %s", evaluation_id)
    except asyncio.TimeoutError:
        await ws.send_json({"type": "error", "message": "Connection timed out waiting for request."})
    except Exception as exc:
        logger.exception("WebSocket error in evaluation %s: %s", evaluation_id, exc)
        try:
            await ws.send_json({"type": "error", "message": str(exc)})
        except Exception:
            pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass
