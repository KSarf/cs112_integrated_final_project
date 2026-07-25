"""Configuration objects for ClinicCare-Lite."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BaseConfig:
    """Base Flask config values."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "replace-with-a-secure-value")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "CLINICCARE_DATABASE_URL", "sqlite:///cliniccare.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024
    UPLOAD_FOLDER: str = str(Path("cliniccare_lite") / "uploads")


class TestingConfig(BaseConfig):
    """Testing config with isolated sqlite db."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config(config_name: str | None = None) -> type[BaseConfig]:
    """Return config class from environment or explicit name."""
    target = config_name or os.getenv("FLASK_ENV", "development")
    if target == "testing":
        return TestingConfig
    return BaseConfig
