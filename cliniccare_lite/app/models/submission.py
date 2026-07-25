"""Submission model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Submission(db.Model):
    """Patient submission placeholder model."""

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
