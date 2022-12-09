from datetime import datetime

from flask_login import current_user
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload


from app import db
from app.models import User, NoteBook, Note, Tag, NoteTags


def create_note(form, title):
    """
    Creating new record for users record book
    :param form: NewNoteForm instance.\n
    :return: None
    """
    book = read_note_book(title, current_user)

    tags = []
    for tag in form.tags.data:
        tag_name = tag.get("tag_name")
        if tag_name:
            tags.append(Tag(tag_name=tag_name))

    note = Note(
        note_title=form.note_title.data,
        text=form.text.data,
        created_at=datetime.now(),
        edited_at=None,
        tags=tags,
        book=book
    )
    db.session.add(note)
    db.session.commit()


def create_note_book(form, user):
    book = NoteBook(
        title=form.title.data,
        user=user
    )
    db.session.add(book)
    db.session.commit()


def read_note_book(title: str, user) -> NoteBook | None:
    """

    :param title: desired book title
    :param user: current user
    :return: NoteBook instance or 404
    """
    return NoteBook.query \
        .join("user") \
        .filter(
            and_(User.username == user.username, NoteBook.title == title)
        ) \
        .first()


def read_note(title, user, note_title) -> Note | None:
    """

    :param title: note book title.
    :param user:  note book owner.!!! Instance, not name!!!
    :param note_title:  title of desired note.
    :return: Record object or 404
    """
    return Note.query \
        .options(joinedload("tags")) \
        .join(NoteBook, and_(Note.book_id == NoteBook.id, NoteBook.title == title)) \
        .join(User, NoteBook.username_id == User.id) \
        .filter(Note.note_title == note_title) \
        .first()


def update_note_book(title: str, book: NoteBook):
    book.title = title
    db.session.commit()


def update_note(note: Note, form):

    tags = []
    for tag in form.tags.data:
        tag_name = tag.get("tag_name")
        if tag_name:
            tags.append(Tag(tag_name=tag_name))


    note.note_title=form.note_title.data
    note.text=form.text.data
    note.edited_at=datetime.now()
    note.tags=tags

    db.session.add(note)
    db.session.commit()


def delete_note_book(book: NoteBook):
    db.session.delete(book)
    db.session.commit()


def delete_note(record: Note):
    db.session.delete(record)
    db.session.commit()
