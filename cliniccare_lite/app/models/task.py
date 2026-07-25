"""Task model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Task(db.Model):
    """Administrative task assigned within clinic workflows."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
