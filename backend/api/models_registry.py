"""Model registry endpoint — returns metadata for all supported models."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/models", tags=["Models"])


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    tier: str
    description: str
    context_window: int
    max_output_tokens: int
    cost_per_1k_input_usd: float
    cost_per_1k_output_usd: float
    supports_arabic: bool
    arabic_native: bool
    available: bool


REGISTRY: List[ModelInfo] = [
    ModelInfo(id="gpt-4o", name="GPT-4o", provider="OpenAI", tier="flagship",
              description="OpenAI's best omni model. Strong Arabic with MSA and Egyptian dialects.",
              context_window=128000, max_output_tokens=4096,
              cost_per_1k_input_usd=0.005, cost_per_1k_output_usd=0.015,
              supports_arabic=True, arabic_native=False, available=True),
    ModelInfo(id="claude-3-5-sonnet", name="Claude 3.5 Sonnet", provider="Anthropic", tier="flagship",
              description="Anthropic's top model. Excellent Arabic quality and cultural awareness.",
              context_window=200000, max_output_tokens=8096,
              cost_per_1k_input_usd=0.003, cost_per_1k_output_usd=0.015,
              supports_arabic=True, arabic_native=False, available=True),
    ModelInfo(id="gemini-1.5-pro", name="Gemini 1.5 Pro", provider="Google", tier="flagship",
              description="Google's multimodal model. Good MSA, weaker on dialects.",
              context_window=1000000, max_output_tokens=8192,
              cost_per_1k_input_usd=0.00125, cost_per_1k_output_usd=0.005,
              supports_arabic=True, arabic_native=False, available=True),
    ModelInfo(id="jais-30b", name="Jais 30B", provider="G42 / MBZUAI", tier="arabic-native",
              description="First Arabic-native LLM. Trained on massive Arabic corpus. Best dialect coverage.",
              context_window=4096, max_output_tokens=2048,
              cost_per_1k_input_usd=0.001, cost_per_1k_output_usd=0.002,
              supports_arabic=True, arabic_native=True, available=True),
    ModelInfo(id="llama-3-70b", name="LLaMA 3 70B", provider="Meta", tier="open-source",
              description="Meta's open-source model. Decent MSA, limited dialect support.",
              context_window=8192, max_output_tokens=2048,
              cost_per_1k_input_usd=0.0004, cost_per_1k_output_usd=0.0008,
              supports_arabic=True, arabic_native=False, available=True),
    ModelInfo(id="mistral-large", name="Mistral Large", provider="Mistral AI", tier="challenger",
              description="Mistral's largest model. Good multilingual including Arabic.",
              context_window=32768, max_output_tokens=4096,
              cost_per_1k_input_usd=0.002, cost_per_1k_output_usd=0.006,
              supports_arabic=True, arabic_native=False, available=True),
]


@router.get("", response_model=List[ModelInfo], summary="List all available models")
async def list_models() -> List[ModelInfo]:
    """Return metadata for all models supported by the evaluation platform."""
    return REGISTRY


@router.get("/{model_id}", response_model=ModelInfo, summary="Get model details")
async def get_model(model_id: str) -> ModelInfo:
    from fastapi import HTTPException
    model = next((m for m in REGISTRY if m.id == model_id), None)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return model
