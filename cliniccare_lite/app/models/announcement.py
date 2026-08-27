"""Clinic announcement model."""

from datetime import datetime

from cliniccare_lite.app.extensions import db


class Announcement(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    body = db.Column(
        db.Text,
        nullable=False,
    )

    priority = db.Column(
        db.String(20),
        nullable=False,
        default="Routine",
    )

    published_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    clinician_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )
