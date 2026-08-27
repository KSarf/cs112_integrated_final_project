"""Configuration helpers for GridCare-Lite."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GridCareConfig:
    """Configuration values loaded from environment."""

    database_path: Path
    enable_demo_login: bool


def load_config() -> GridCareConfig:
    """Load GridCare configuration from environment variables."""
    database_value = os.getenv(
        "GRIDCARE_DATABASE_PATH", "gridcare_lite/database/gridcare.db"
    )
    demo_login_value = os.getenv("GRIDCARE_ENABLE_DEMO_LOGIN", "false").lower()

    return GridCareConfig(
        database_path=Path(database_value),
        enable_demo_login=demo_login_value == "true",
    )
