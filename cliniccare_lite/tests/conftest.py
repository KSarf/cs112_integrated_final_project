"""Shared test fixtures for ClinicCare-Lite."""

from __future__ import annotations

import pytest

from cliniccare_lite.app import create_app


@pytest.fixture()
def app():
    """Create test Flask app instance."""
    flask_app = create_app("testing")
    yield flask_app


@pytest.fixture()
def client(app):
    """Create Flask test client."""
    return app.test_client()
