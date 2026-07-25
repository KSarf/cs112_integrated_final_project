"""Patient routes for ClinicCare-Lite."""

from __future__ import annotations

from flask import Blueprint, render_template

patient_bp = Blueprint("patient", __name__, template_folder="../templates")


@patient_bp.route("/dashboard")
def dashboard() -> str:
    """Render patient dashboard placeholder."""
    return render_template("patient/dashboard.html")
