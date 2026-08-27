"""Forms for ClinicCare-Lite authentication."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "User ID",
        validators=[
            DataRequired(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """Registration form."""

    username = StringField(
        "User ID",
        validators=[
            DataRequired(),
        ],
    )

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=120,
            ),
        ],
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Length(max=120),
            Regexp(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                message="Enter a valid email address.",
            ),
        ],
    )

    role = SelectField(
        "Account Type",
        choices=[
            ("patient", "Patient"),
            ("clinician", "Clinician"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=128,
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match.",
            ),
        ],
    )

    submit = SubmitField("Create Account")

    def validate_username(
        self,
        field,
    ):
        """Validate clinician and patient ID formats."""

        user_id = field.data.strip()

        if len(user_id) != 8 or not user_id.isdigit():
            raise ValidationError("User ID must contain exactly 8 digits.")

        if self.role.data == "clinician":

            if not user_id.endswith("0000"):
                raise ValidationError("Clinician IDs must end in 0000.")

        elif self.role.data == "patient":

            year = int(user_id[-4:])

            if year < 2022 or year > 2028:
                raise ValidationError(
                    "Patient IDs must end in a " "registration year from 2022 to 2028."
                )

    def validate_password(
        self,
        field,
    ):
        """Validate password complexity."""

        password = field.data

        special_characters = "!@#$%^&*()-_=+[]{}:;,.?/"

        if not any(character.isupper() for character in password):
            raise ValidationError("Password must contain an uppercase letter.")

        if not any(character.islower() for character in password):
            raise ValidationError("Password must contain a lowercase letter.")

        if not any(character.isdigit() for character in password):
            raise ValidationError("Password must contain a number.")

        if not any(character in special_characters for character in password):
            raise ValidationError("Password must contain a special character.")
