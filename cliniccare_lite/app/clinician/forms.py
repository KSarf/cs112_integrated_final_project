from flask_wtf import FlaskForm

from wtforms import (
    DateTimeLocalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)

from wtforms.validators import DataRequired


class TaskForm(FlaskForm):

    patient_username = StringField(
        "Patient Username",
        validators=[DataRequired()]
    )

    title = StringField(
        "Task Title",
        validators=[DataRequired()]
    )

    instructions = TextAreaField(
        "Instructions",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Create Task"
    )


class ReviewSubmissionForm(FlaskForm):

    status = SelectField(
        "Review Result",
        choices=[
            ("Reviewed", "Reviewed"),
            (
                "Needs Resubmission",
                "Needs Resubmission"
            ),
        ],
        validators=[DataRequired()]
    )

    review_notes = TextAreaField(
        "Review Notes",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Save Review"
    )


class AppointmentForm(FlaskForm):

    patient_username = StringField(
        "Patient Username",
        validators=[DataRequired()]
    )

    summary = StringField(
        "Appointment Purpose",
        validators=[DataRequired()]
    )

    appointment_time = DateTimeLocalField(
        "Appointment Date and Time",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Schedule Appointment"
    )