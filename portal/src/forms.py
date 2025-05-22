import re

import sqlalchemy as sa
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NoneOf, ValidationError

from . import db
from .models import User

RFC1123_PATTERN = re.compile(r"[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*")


def rfc1123(_, field):
    match = RFC1123_PATTERN.match(field.data)
    if match is None or match.group() != field.data:
        raise ValidationError(
            "Username must be valid RFC1123 style, this means: \n"
            "\tconsist of lower case alphanumeric characters, '-' or '.', and\n"
            "\tmust start and end with an alphanumeric character"
        )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            NoneOf(
                values=[
                    "devplayer",
                ],
                message="this username is not allowed.",
            ),
            rfc1123,
            Length(min=4, max=64),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")
