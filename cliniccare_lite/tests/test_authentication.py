"""Route tests for ClinicCare-Lite starter pages."""

from __future__ import annotations


def test_core_routes_respond(client) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/login").status_code == 200
    assert client.get("/clinician/dashboard").status_code == 200
    assert client.get("/patient/dashboard").status_code == 200
