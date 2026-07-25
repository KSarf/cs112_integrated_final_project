"""User model for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """Application user."""

    id: int | None
    username: str
    role: str
