"""Clinician routes for ClinicCare-Lite."""

from __future__ import annotations

from flask import Blueprint, render_template

clinician_bp = Blueprint("clinician", __name__, template_folder="../templates")


@clinician_bp.route("/dashboard")
def dashboard() -> str:
    """Render clinician dashboard placeholder."""
    return render_template("clinician/dashboard.html")
