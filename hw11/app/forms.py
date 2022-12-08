import re

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, DateField, TelField, \
    TextAreaField, DateTimeField
from wtforms.validators import ValidationError, EqualTo, DataRequired, Optional

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
        if book:
            raise ValidationError(f"Book with title {book_title} already exists.")


class EditRecordBookForm(NewRecordBookForm):
    submit = SubmitField("Edit")


class PhoneForm(FlaskForm):
    value = StringField("phone number", description="0123456789", validators=[Optional(strip_whitespace=False)])

    def validate_field(self, value):
        number = value.data
        if number is None:
            raise ValidationError("You forgot to enter the number")
        if len(number) != 10:
            raise ValidationError("Number must be 10 digits.")
        if not number.isdigit():
            raise ValidationError("Number must contain only digits")


class EmailForm(FlaskForm):
    value = StringField("email", description="example@mail.com", validators=[Optional(strip_whitespace=False)])

    def validate_field(self, value):
        email = value.data
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
            phones: list = read_form_data["phones"]
            new_phone = phones[-1].get("value")

            if len(new_phone) != 10 and not new_phone.isdigit():
                phones.pop()  # if not validated do not add new field
            else:
                phones.append({})
            read_form_data["phones"] = phones

        if read_form_data["new_email"]:
            emails: list = read_form_data['emails']
            new_email = emails[-1].get("value")
            __pattern = r"^[a-zA-Z][\w.]{1,}@([a-zA-Z]{2,}[.][a-zA-Z]{2,}|[a-zA-Z]{2,}[.][a-zA-Z]{2,}[.][a-zA-Z]{2,})$"
            if re.match(__pattern, new_email):
                emails.append({})  # if not validated do not add new field
            else:
                emails.pop()
            read_form_data["emails"] = emails

        self.__init__(formdata=None, **read_form_data)  # reload the form from modified data
        self.validate()


class EditRecordForm(NewRecordForm):
    submit = SubmitField("Save changes")


class NewNoteBookForm(FlaskForm):

    title = StringField("Note book name", validators=[DataRequired(message="Enter book name")])
    submit = SubmitField("Create")

    def validate_title(self, title):
        book_title = title.data
        book = crud.read_note_book(book_title, current_user)
        if book:
            raise ValidationError(f"Book with title {book_title} already exists.")


class EditNoteBookForm(NewNoteBookForm):
    submit = SubmitField("Edit")


class TagForm(FlaskForm):

    name = StringField("Tag name", validators=[Optional(strip_whitespace=False)])

class NewNoteForm(FlaskForm):

    note_title = StringField("Note book title", validators=[DataRequired()])
    text = TextAreaField("Note text", validators=[Optional()])
    created_at = DateTimeField("Created at:")
    tags = FieldList()
    submit = SubmitField("Create note")