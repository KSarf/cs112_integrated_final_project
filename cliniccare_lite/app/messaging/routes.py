"""Messaging routes for ClinicCare-Lite."""

from __future__ import annotations

from flask import Blueprint

messaging_bp = Blueprint("messaging", __name__)


@messaging_bp.route("/")
def inbox() -> str:
    """Return starter messaging placeholder response."""
    return "TODO: Implement non-urgent messaging inbox."
