"""
FastAPI dependency injection — shared dependencies for route handlers.
"""

import logging
from typing import Optional
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_api_key, extract_api_key_from_header
from app.models.user import APIKey, User

logger = logging.getLogger(__name__)


async def get_current_api_key(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> APIKey:
    """
    Dependency: validate Bearer API key from Authorization header.
    Raises 401 if missing or invalid.
    """
    raw_key = extract_api_key_from_header(authorization)
    if not raw_key:
        raise HTTPException(
            status_code=401,
            detail={"code": "MISSING_API_KEY", "message": "Authorization header required."},
        )

    # Look up all active keys (we hash and compare)
    result = await db.execute(
        select(APIKey).where(APIKey.is_active == True)
    )
    keys = result.scalars().all()

    matched_key: Optional[APIKey] = None
    for key in keys:
        if verify_api_key(raw_key, key.key_hash):
            matched_key = key
            break

    if not matched_key:
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_API_KEY", "message": "Invalid or expired API key."},
        )

    if matched_key.is_expired:
        raise HTTPException(
            status_code=401,
            detail={"code": "EXPIRED_API_KEY", "message": "This API key has expired."},
        )

    logger.debug("Authenticated via key prefix=%s", matched_key.prefix)
    return matched_key


async def get_optional_api_key(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> Optional[APIKey]:
    """Optional authentication — returns None instead of raising 401."""
    try:
        return await get_current_api_key(authorization=authorization, db=db)
    except HTTPException:
        return None
