"""
LLM-Eval-Arabic — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.api import health, evaluations, models_registry, benchmarks, streaming


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info(
        "Starting %s v%s (%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


# ── App instance ──────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "المنصة العربية لتقييم نماذج اللغة الكبيرة\n\n"
        "The definitive Arabic LLM evaluation platform. "
        "Compare GPT-4o, Claude, Gemini, Jais, and more across 6 Arabic dialects "
        "with automated LLM-as-Judge scoring."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ── Exception handlers ────────────────────────────────────
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── Routers ───────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(evaluations.router, prefix=API_PREFIX)
app.include_router(models_registry.router, prefix=API_PREFIX)
app.include_router(benchmarks.router, prefix=API_PREFIX)
app.include_router(streaming.router)   # WebSocket — no prefix

# ── Root ──────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
        "arabic": "المنصة العربية لتقييم نماذج اللغة",
    }
