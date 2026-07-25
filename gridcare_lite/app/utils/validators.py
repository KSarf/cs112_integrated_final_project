"""Input-validation helpers for GridCare-Lite."""

from __future__ import annotations


def is_non_empty(value: str) -> bool:
    """Check that a string contains non-whitespace text."""
    return bool(value and value.strip())
