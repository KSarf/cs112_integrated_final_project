"""Tests for upload validation helpers."""

from __future__ import annotations

from cliniccare_lite.app.uploads.validators import is_allowed_extension, sanitize_filename


def test_allowed_extensions_and_filename_sanitization() -> None:
    assert is_allowed_extension("report.pdf")
    assert is_allowed_extension("notes.TXT")
    assert not is_allowed_extension("image.png")
    assert sanitize_filename("../../secret.txt") == "secret.txt"
