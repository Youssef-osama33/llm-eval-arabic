"""
API key generation, hashing, and verification.
Keys are hashed with bcrypt before database storage.
"""

import secrets
import hashlib
from datetime import datetime, timezone
from typing import Optional

from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_api_key() -> tuple[str, str]:
    """
    Generate a new API key.
    Returns (raw_key, hashed_key).
    The raw_key is shown to the user once; hashed_key is stored.
    """
    raw_key = f"eval_{secrets.token_urlsafe(settings.API_KEY_LENGTH)}"
    hashed = hashlib.sha256(raw_key.encode()).hexdigest()
    return raw_key, hashed


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    """Verify a raw API key against its stored hash."""
    try:
        candidate_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        return secrets.compare_digest(candidate_hash, stored_hash)
    except Exception:
        return False


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def extract_api_key_from_header(authorization: Optional[str]) -> Optional[str]:
    """
    Extract API key from 'Authorization: Bearer <key>' header.
    Returns None if the header is missing or malformed.
    """
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]
