from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class SubmissionForm(FlaskForm):

    file = FileField(
        "Upload File",
        validators=[FileRequired()]
    )

    submit = SubmitField("Submit File")