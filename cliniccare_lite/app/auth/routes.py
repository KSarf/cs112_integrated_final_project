"""Authentication routes for ClinicCare-Lite."""


from __future__ import annotations
from flask_login import login_required
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user, login_user
from flask_login import current_user, login_required

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.user import User

from .forms import LoginForm


auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.execute(
            db.select(User).where(User.username == form.username.data)
        ).scalar_one_or_none()

        if user and user.check_password(form.password.data):
            login_user(user)

            if user.role == "clinician":
                return redirect(url_for("clinician.dashboard"))

            return redirect(url_for("patient.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))
