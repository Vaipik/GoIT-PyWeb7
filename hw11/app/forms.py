import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, Form, FormField, DateField
from wtforms.validators import ValidationError, EqualTo, DataRequired, Optional, Length, InputRequired

from .models import User, RecordBook


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
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise ValidationError("User already exists. Try another username")


class NewRecordBookForm(FlaskForm):

    book_name = StringField("Record book name", validators=[DataRequired(message="Enter book name")])
    submit = SubmitField("Create")

    def validate_book_name(self, book_name):
        book = User.query.filter_by(book_name=book_name).first()
        if book is not None:
            raise ValidationError("Record book already exists. Try another ")


class PhoneForm(FlaskForm):
    number = StringField("number", validators=[DataRequired()])

    def validate_number(self, number):
        num = number.data
        print(num)
        if num is None:
            print(f"{num} not valid - empty")
            raise ValidationError("You forgot to enter the number")
        if len(num) != 10 and not num.isdigit():
            print(f"{num} not valid - not number")
            raise ValidationError("Number must be 10 digits.")


class EmailForm(FlaskForm):
    email = StringField("email", validators=[Optional(strip_whitespace=False)])

    def validate_email(self, email):
        __pattern = r"^[a-zA-Z][\w.]{1,}@([a-zA-Z]{2,}[.][a-zA-Z]{2,}|[a-zA-Z]{2,}[.][a-zA-Z]{2,}[.][a-zA-Z]{2,})$"
        if email.data is None:
            raise ValidationError("You forgot to enter the number")
        if not re.match(__pattern, email.data):
            raise ValidationError("Wrong email. Try again.")


class NewRecordForm(FlaskForm):

    name = StringField("Contact name", validators=[DataRequired(message="Enter contact name")])
    birthday = DateField("Birthday", validators=[Optional()])
    phones = FieldList(FormField(PhoneForm), min_entries=1, max_entries=5, validators=[Optional(strip_whitespace=False)])
    emails = FieldList(FormField(EmailForm), min_entries=1, max_entries=5, validators=[Optional(strip_whitespace=False)])
    submit = SubmitField("Add new record")
    new_phone = SubmitField("Add new phone")
    new_email = SubmitField("Add new email")

    def update_self(self):

        read_form_data = self.data

        if read_form_data['new_phone']:
            new_phone = read_form_data['phones']
            new_phone.append({})
            read_form_data['phones'] = new_phone

        if read_form_data['new_email']:
            new_email = read_form_data['emails']
            new_email.append({})
            read_form_data['emails'] = new_email

        self.__init__(formdata=None, **read_form_data)  # reload the form from modified data
        self.validate()
