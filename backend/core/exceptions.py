"""
Custom application exceptions with structured HTTP responses.
All exceptions map to specific HTTP status codes and error codes.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        detail: Optional[Any] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class EvaluationNotFoundError(AppException):
    def __init__(self, evaluation_id: str):
        super().__init__(
            message=f"Evaluation '{evaluation_id}' not found.",
            error_code="EVALUATION_NOT_FOUND",
            status_code=404,
        )


class ModelNotAvailableError(AppException):
    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model '{model_id}' is not available or misconfigured.",
            error_code="MODEL_NOT_AVAILABLE",
            status_code=422,
        )


class InvalidPromptError(AppException):
    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid prompt: {reason}",
            error_code="INVALID_PROMPT",
            status_code=400,
        )


class RateLimitExceededError(AppException):
    def __init__(self):
        super().__init__(
            message="Rate limit exceeded. Please wait before making more requests.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )


class AuthenticationError(AppException):
    def __init__(self, reason: str = "Invalid or missing API key."):
        super().__init__(
            message=reason,
            error_code="AUTHENTICATION_FAILED",
            status_code=401,
        )


class EvaluationTimeoutError(AppException):
    def __init__(self, model_id: str, timeout: int):
        super().__init__(
            message=f"Model '{model_id}' timed out after {timeout}s.",
            error_code="EVALUATION_TIMEOUT",
            status_code=504,
        )


class ScoringError(AppException):
    def __init__(self, reason: str):
        super().__init__(
            message=f"Scoring failed: {reason}",
            error_code="SCORING_FAILED",
            status_code=500,
        )


# ── FastAPI exception handlers ────────────────────────────

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "detail": exc.detail,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
                "detail": str(exc) if not isinstance(exc, HTTPException) else None,
            }
        },
    )
