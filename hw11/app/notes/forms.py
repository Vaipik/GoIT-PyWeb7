from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, TextAreaField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Optional


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