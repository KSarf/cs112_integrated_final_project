"""Submission model for ClinicCare-Lite."""

from datetime import datetime

from cliniccare_lite.app.extensions import db


class Submission(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("task.id"),
        nullable=False,
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    file_name = db.Column(
        db.String(255),
        nullable=False,
    )

    status = db.Column(
        db.String(40),
        nullable=False,
        default="Submitted",
    )

    submitted_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    review_notes = db.Column(
        db.Text,
        nullable=True,
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True,
    )
