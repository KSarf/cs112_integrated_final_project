"""Authentication routes for ClinicCare-Lite."""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for

from .forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Render and process starter login form.

    TODO: Implement secure authentication workflow.
    """
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=form)
