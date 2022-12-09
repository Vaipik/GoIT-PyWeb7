from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, TextAreaField, DateTimeField, FormField
from wtforms.validators import ValidationError, DataRequired, Optional

from . import crud


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
    tag_name = StringField("Tag name", validators=[Optional(strip_whitespace=False)])


class NewNoteForm(FlaskForm):

    note_title = StringField("Note book title", validators=[DataRequired()])
    text = TextAreaField("Note text", validators=[Optional()])
    tags = FieldList(FormField(TagForm), min_entries=1, max_entries=5)
    submit = SubmitField("Create note")
    new_tag = SubmitField("Add new tag")

    def update_self(self):

        read_form_data = self.data

        if read_form_data["new_tag"]:

            tags: list = read_form_data["tags"]
            print(tags)
            new_tag = tags[-1].get("tag_name")
            if new_tag:
                tags.append({})
            else:
                tags.pop()

            read_form_data["tags"] = tags

        self.__init__(formdata=None, **read_form_data)  # reload the form from modified data
        self.validate()


class EditNoteForm(NewNoteForm):
    submit = SubmitField("Edit")
