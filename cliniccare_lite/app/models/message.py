"""Message model for ClinicCare-Lite."""

from datetime import datetime

from cliniccare_lite.app.extensions import db


class Message(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    body = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )
