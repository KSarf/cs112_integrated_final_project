"""Role and permission helpers for GridCare-Lite."""

from __future__ import annotations

ROLE_ADMINISTRATOR = "Administrator"
ROLE_ENGINEER = "Engineer"
ROLE_TECHNICIAN = "Technician"
ROLE_CUSTOMER_SERVICE_REPRESENTATIVE = "Customer-service representative"

PERMISSIONS: dict[str, set[str]] = {
    ROLE_ADMINISTRATOR: {"view_dashboard", "manage_users", "assign_work_orders"},
    ROLE_ENGINEER: {"view_dashboard", "manage_outages", "assign_work_orders"},
    ROLE_TECHNICIAN: {"view_dashboard", "update_work_orders"},
    ROLE_CUSTOMER_SERVICE_REPRESENTATIVE: {"view_dashboard", "log_complaints"},
}


def has_permission(role: str, permission: str) -> bool:
    """Return whether role grants a specific permission."""
    return permission in PERMISSIONS.get(role, set())
