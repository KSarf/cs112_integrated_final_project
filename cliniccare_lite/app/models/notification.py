"""Notification model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Notification(db.Model):
    """Administrative notification placeholder."""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
