"""Authentication routes for ClinicCare-Lite."""

from __future__ import annotations

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.user import User

from .forms import (
    LoginForm,
    RegistrationForm,
)

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates",
)


def redirect_to_dashboard():
    """Send a user to the correct dashboard."""

    if current_user.role == "clinician":
        return redirect(url_for("clinician.dashboard"))

    return redirect(url_for("patient.dashboard"))


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    """Log a user into ClinicCare-Lite."""

    if current_user.is_authenticated:
        return redirect_to_dashboard()

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data.strip()

        user = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()

        if user and user.check_password(form.password.data):

            login_user(user)

            flash(
                "Login successful.",
                "success",
            )

            return redirect_to_dashboard()

        flash(
            "Invalid username or password.",
            "danger",
        )

    return render_template(
        "auth/login.html",
        form=form,
    )


@auth_bp.route(
    "/register",
    methods=["GET", "POST"],
)
def register():
    """Register a new user."""

    if current_user.is_authenticated:
        return redirect_to_dashboard()

    form = RegistrationForm()

    if form.validate_on_submit():

        username = form.username.data.strip()

        email = form.email.data.strip().lower()

        existing_user = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()

        if existing_user:

            flash(
                "That User ID is already registered.",
                "danger",
            )

            return render_template(
                "auth/register.html",
                form=form,
            )

        existing_email = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing_email:

            flash(
                "That email address is already registered.",
                "danger",
            )

            return render_template(
                "auth/register.html",
                form=form,
            )

        user = User()

        user.username = username
        user.full_name = form.full_name.data.strip()
        user.email = email
        user.role = form.role.data

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully. " "You can now log in.",
            "success",
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form,
    )


@auth_bp.route("/logout")
@login_required
def logout():
    """Log the current user out."""

    logout_user()

    flash(
        "Logged out successfully.",
        "info",
    )

    return redirect(url_for("auth.login"))
