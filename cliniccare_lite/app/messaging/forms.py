from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):

    recipient_username = StringField(
        "Recipient Username",
        validators=[DataRequired()]
    )

    body = TextAreaField(
        "Message",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Send Message"
    )