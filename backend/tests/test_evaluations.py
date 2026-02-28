"""Integration tests for evaluation API endpoints."""

import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_list_models(client: AsyncClient):
    response = await client.get("/api/v1/models")
    assert response.status_code == 200
    models = response.json()
    assert isinstance(models, list)
    assert len(models) > 0
    assert all("id" in m for m in models)


@pytest.mark.asyncio
async def test_evaluation_create_validation_min_models(client: AsyncClient):
    """Should fail with only 1 model (minimum is 2)."""
    response = await client.post("/api/v1/evaluations/run", json={
        "prompt": "اشرح مفهوم الذكاء الاصطناعي",
        "dialect": "msa",
        "category": "technical_terminology",
        "models": ["gpt-4o"],  # only 1 — should fail
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_evaluation_create_validation_bad_dialect(client: AsyncClient):
    response = await client.post("/api/v1/evaluations/run", json={
        "prompt": "اشرح مفهوم الذكاء الاصطناعي",
        "dialect": "klingon",  # invalid
        "models": ["gpt-4o", "claude-3-5-sonnet"],
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_evaluation_create_validation_short_prompt(client: AsyncClient):
    response = await client.post("/api/v1/evaluations/run", json={
        "prompt": "مرحبا",  # too short (< 10 chars)
        "dialect": "msa",
        "models": ["gpt-4o", "claude-3-5-sonnet"],
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_evaluation(client: AsyncClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/evaluations/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_evaluations_pagination(client: AsyncClient):
    response = await client.get("/api/v1/evaluations?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["page"] == 1
