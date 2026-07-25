"""Appointment model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Appointment(db.Model):
    """Administrative appointment scheduling record."""

    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(255), nullable=False)
