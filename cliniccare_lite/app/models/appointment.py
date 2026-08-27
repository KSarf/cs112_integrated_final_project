from cliniccare_lite.app.extensions import db


class Appointment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
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

    summary = db.Column(
        db.String(255),
        nullable=False
    )

    appointment_time = db.Column(
        db.DateTime,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Scheduled"
    )