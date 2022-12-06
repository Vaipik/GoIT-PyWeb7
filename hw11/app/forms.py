import re

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, Form, FormField, DateField
from wtforms.validators import ValidationError, EqualTo, DataRequired, Optional, Length, InputRequired

from .models import User
from . import crud


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

    title = StringField("Record book name", validators=[DataRequired(message="Enter book name")])
    submit = SubmitField("Create")

    def validate_title(self, title):
        book_title = title.data
        book = crud.read_record_book(book_title, current_user)
        # print(book)
        if book:
            raise ValidationError(f"Book with title {book_title} already exists.")


class PhoneForm(FlaskForm):
    field = StringField("phone number", description="0123456789", validators=[Optional(strip_whitespace=False)])

    def validate_field(self, field):
        number = field.data
        if number is None:
            raise ValidationError("You forgot to enter the number")
        if len(number) != 10:
            raise ValidationError("Number must be 10 digits.")
        if not number.isdigit():
            raise ValidationError("Number must contain only digits")


class EmailForm(FlaskForm):
    field = StringField("email", description="example@mail.com", validators=[Optional(strip_whitespace=False)])

    def validate_field(self, field):
        email = field.data
        __pattern = r"^[a-zA-Z][\w.]{1,}@([a-zA-Z]{2,}[.][a-zA-Z]{2,}|[a-zA-Z]{2,}[.][a-zA-Z]{2,}[.][a-zA-Z]{2,})$"
        if email is None:
            raise ValidationError("You forgot to enter the number")
        if not re.match(__pattern, email):
            raise ValidationError("Wrong email. Try again.")


class NewRecordForm(FlaskForm):

    name = StringField("Contact name", description="Enter name in this field", validators=[DataRequired(message="Enter contact name")])
    birthday = DateField("Birthday", validators=[Optional()])
    phones = FieldList(FormField(PhoneForm, label="Phone number"), min_entries=1, max_entries=5)
    emails = FieldList(FormField(EmailForm), min_entries=1, max_entries=5)
    submit = SubmitField("Add new record")
    new_phone = SubmitField("Add new phone")
    new_email = SubmitField("Add new email")

    def update_self(self):

        read_form_data = self.data

        if read_form_data["new_phone"]:
            print("WTF")
            phones: list = read_form_data["phones"]
            new_phone = phones[-1].get("field")
            if len(new_phone) != 10 and not new_phone.isdigit():
                phones.pop()  # if not validated do not add new field
            else:
                phones.append({})
            read_form_data["phones"] = phones

        if read_form_data['new_email']:
            emails: list = read_form_data['emails']
            new_email = emails[-1].get("field")
            __pattern = r"^[a-zA-Z][\w.]{1,}@([a-zA-Z]{2,}[.][a-zA-Z]{2,}|[a-zA-Z]{2,}[.][a-zA-Z]{2,}[.][a-zA-Z]{2,})$"
            if re.match(__pattern, new_email):
                emails.append({})  # if not validated do not add new field
            else:
                emails.pop()
            read_form_data["emails"] = emails

        self.__init__(formdata=None, **read_form_data)  # reload the form from modified data
        self.validate()
