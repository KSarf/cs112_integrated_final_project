"""Task model for ClinicCare-Lite."""

from cliniccare_lite.app.extensions import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    instructions = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    clinician_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )