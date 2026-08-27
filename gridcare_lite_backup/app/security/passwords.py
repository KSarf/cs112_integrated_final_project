"""Password helpers based on bcrypt."""

from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    encoded_password = password.encode("utf-8")
    hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify plaintext password against bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
