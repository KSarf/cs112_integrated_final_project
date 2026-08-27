"""Tests for GridCare-Lite permissions."""

from __future__ import annotations

from gridcare_lite.app.security.permissions import (
    ROLE_ADMINISTRATOR,
    ROLE_TECHNICIAN,
    has_permission,
)


def test_role_permissions() -> None:
    assert has_permission(ROLE_ADMINISTRATOR, "manage_users")
    assert not has_permission(ROLE_TECHNICIAN, "manage_users")
