from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, EqualTo, DataRequired

from app.auth import crud


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(message="Enter username")])
    password = PasswordField("Password", validators=[DataRequired(message="Enter password")])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password", message="Do not match")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = crud.read_user(username.data)
        if user is not None:
            raise ValidationError("User already exists. Try another username")