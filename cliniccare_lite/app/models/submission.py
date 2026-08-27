"""Submission model placeholder."""

from __future__ import annotations

from cliniccare_lite.app.extensions import db


class Submission(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("task.id"),
        nullable=False
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(40),
        nullable=False,
        default="Submitted"
    )

    review_notes = db.Column(
        db.Text,
        nullable=True
    )