"""Application factory for ClinicCare-Lite."""

from __future__ import annotations

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge

from .auth.routes import auth_bp
from .clinician.routes import clinician_bp
from .config import get_config
from .extensions import (
    bcrypt,
    csrf,
    db,
    login_manager,
)
from .messaging.routes import messaging_bp
from .patient.routes import patient_bp


def create_app(
    config_name: str | None = None,
) -> Flask:
    """Create and configure Flask application."""

    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    app.config.from_object(get_config(config_name))

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)

    app.register_blueprint(
        clinician_bp,
        url_prefix="/clinician",
    )

    app.register_blueprint(
        patient_bp,
        url_prefix="/patient",
    )

    app.register_blueprint(
        messaging_bp,
        url_prefix="/messaging",
    )

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(
        _error,
    ):

        flash(
            "File is too large. " "The maximum upload size is 10 MB.",
            "danger",
        )

        return redirect(url_for("patient.dashboard"))

    with app.app_context():

        from . import models  # noqa: F401

        db.create_all()

    return app
