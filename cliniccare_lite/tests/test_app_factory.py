"""Tests for ClinicCare-Lite application factory."""

from __future__ import annotations

from cliniccare_lite.app import create_app


def test_create_app_testing_config() -> None:
    app = create_app("testing")
    assert app.config["TESTING"] is True
    assert app.config["WTF_CSRF_ENABLED"] is False
