from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DateTimeLocalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
)


class TaskForm(FlaskForm):

    patient_username = StringField(
        "Patient User ID",
        validators=[
            DataRequired(),
        ],
    )

    title = StringField(
        "Task Title",
        validators=[
            DataRequired(),
        ],
    )

    instructions = TextAreaField(
        "Instructions",
        validators=[
            DataRequired(),
        ],
    )

    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Create Task")


class ReviewSubmissionForm(FlaskForm):

    status = SelectField(
        "Review Result",
        choices=[
            (
                "Reviewed",
                "Reviewed",
            ),
            (
                "Needs Follow-up",
                "Needs Follow-up",
            ),
            (
                "Needs Resubmission",
                "Needs Resubmission",
            ),
            (
                "Escalated",
                "Escalated",
            ),
        ],
        validators=[
            DataRequired(),
        ],
    )

    review_notes = TextAreaField(
        "Review Notes",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Save Review")


class AppointmentForm(FlaskForm):

    patient_username = StringField(
        "Patient User ID",
        validators=[
            DataRequired(),
        ],
    )

    summary = StringField(
        "Appointment Purpose",
        validators=[
            DataRequired(),
        ],
    )

    appointment_time = DateTimeLocalField(
        "Appointment Date and Time",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Schedule Appointment")


class AnnouncementForm(FlaskForm):

    title = StringField(
        "Announcement Title",
        validators=[
            DataRequired(),
        ],
    )

    body = TextAreaField(
        "Announcement Message",
        validators=[
            DataRequired(),
        ],
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Routine", "Routine"),
            ("Urgent", "Urgent"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    expires_at = DateTimeLocalField(
        "Expiry Date and Time",
        format="%Y-%m-%dT%H:%M",
        validators=[
            Optional(),
        ],
    )

    submit = SubmitField("Publish Announcement")
