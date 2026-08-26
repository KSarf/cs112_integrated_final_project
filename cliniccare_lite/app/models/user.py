"""User model for ClinicCare-Lite."""

from __future__ import annotations
from flask_login import UserMixin
from cliniccare_lite.app.extensions import db, login_manager, bcrypt


class User(db.Model, UserMixin):
    """Application user record."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(225),nullable=False)
    role = db.Column(db.String(40), nullable=False, default="patient")

    def set_password(self, password= str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password = str) -> bool:
        return  bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Load user by id for Flask-Login session management."""
    return db.session.get(User, int(user_id))
