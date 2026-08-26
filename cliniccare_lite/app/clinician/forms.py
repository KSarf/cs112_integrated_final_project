from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
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

    submit = SubmitField("Create Task")