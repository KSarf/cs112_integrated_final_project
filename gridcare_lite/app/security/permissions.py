"""Role and permission helpers for GridCare-Lite."""

from __future__ import annotations

ROLE_ADMINISTRATOR = "Administrator"
ROLE_ENGINEER = "Engineer"
ROLE_TECHNICIAN = "Technician"
ROLE_CUSTOMER_SERVICE_REPRESENTATIVE = "Customer-service representative"

PERMISSIONS: dict[str, set[str]] = {
    ROLE_ADMINISTRATOR: {
        "view_dashboard",
        "view_substations",
        "view_outages",
        "review_outages",
        "view_work_orders",
        "create_work_orders",
        "manage_users",
        "view_reports",
    },
    ROLE_ENGINEER: {
        "view_dashboard",
        "view_substations",
        "view_outages",
        "create_outages",
    },
    ROLE_TECHNICIAN: {
        "view_dashboard",
        "view_work_orders",
        "update_work_orders",
    },
    ROLE_CUSTOMER_SERVICE_REPRESENTATIVE: {
        "view_dashboard",
        "view_outages",
        "log_complaints",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """Return whether a role has a permission."""
    return permission in PERMISSIONS.get(role, set())
