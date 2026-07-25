"""Message model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Message(db.Model):
    """Non-urgent administrative message."""

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
