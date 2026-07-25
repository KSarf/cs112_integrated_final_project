"""Upload validation helpers for ClinicCare-Lite."""

from __future__ import annotations

from pathlib import Path

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".txt", ".csv", ".pdf"}


def is_allowed_extension(filename: str) -> bool:
    """Return whether a filename has an approved extension."""
    extension = Path(filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS


def sanitize_filename(filename: str) -> str:
    """Safely sanitize a user-provided filename."""
    return secure_filename(filename)
