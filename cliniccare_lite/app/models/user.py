"""User model for ClinicCare-Lite."""

from __future__ import annotations

from flask_login import UserMixin

from cliniccare_lite.app.extensions import (
    bcrypt,
    db,
    login_manager,
)


class User(db.Model, UserMixin):
    """Application user record."""

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(40),
        nullable=False,
        default="patient"
    )

    def set_password(
        self,
        password: str
    ) -> None:
        """Hash and store a user's password."""

        self.password_hash = (
            bcrypt.generate_password_hash(
                password
            ).decode("utf-8")
        )

    def check_password(
        self,
        password: str
    ) -> bool:
        """Check a password against its stored hash."""

        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )


@login_manager.user_loader
def load_user(
    user_id: str
) -> User | None:
    """Load the logged-in user from the session."""

    return db.session.get(
        User,
        int(user_id)
    )