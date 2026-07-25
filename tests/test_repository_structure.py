"""Validate expected starter repository structure."""

from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    Path("grid_analysis/src/grid_analysis/data_validation.py"),
    Path("gridcare_lite/app/main.py"),
    Path("cliniccare_lite/app/__init__.py"),
    Path("docs/security-and-ethics.md"),
    Path(".github/workflows/ci.yml"),
]


def test_required_paths_exist() -> None:
    for path in REQUIRED_PATHS:
        assert path.exists(), f"Missing required path: {path}"
