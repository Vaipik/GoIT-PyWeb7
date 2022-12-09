from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from app import db
from app.models import User, RecordBook, Record, Phone, Email


def create_record(form, title: str, user):
    """
    Creating new record for users record book
    :param form: NewRecordForm instance.\n
    :param title: record book title.\n
    :param user: current user.
    :return: None
    """
    book = read_record_book(title, user)

    phones = []
    for phone in form.phones.data:
        phone_number = phone.get("value")
        if phone_number:
            phones.append(Phone(value=phone_number))

    emails = []
    for email in form.emails.data:
        email_address = email.get("value")
        if email_address:
            emails.append(Email(value=email_address))

    record = Record(
        name=form.name.data,
        birthday=form.birthday.data,
        phones=phones,
        emails=emails,
        book=book
    )

    db.session.add(record)
    db.session.commit()


def create_record_book(form, user):
    book = RecordBook(
        title=form.title.data,
        user=user
    )
    db.session.add(book)
    db.session.commit()


def read_record_book(title: str, user) -> RecordBook | None:
    """

    :param title: desired book title
    :param user: current user
    :return: RecordBook instance or 404
    """
    return RecordBook.query \
        .join("user") \
        .filter(
            and_(User.username == user.username, RecordBook.title == title)
        ) \
        .first()


def read_record(title, user, record_name) -> Record | None:
    """

    :param title: record book title.\n
    :param user:  record book owner.\n
    :param record_name: desired contact.\n
    :return: Record object or 404
    """
    return Record.query \
        .options(joinedload("phones"), joinedload("emails")) \
        .join(RecordBook, and_(Record.book_id == RecordBook.id, RecordBook.title == title)) \
        .join(User, RecordBook.username_id == User.id) \
        .filter(Record.name == record_name) \
        .first()


def update_record_book(title: str, book: RecordBook):
    book.title = title
    db.session.commit()


def update_record(record: Record, form):
    """

    :param record:
    :param form:
    :return:
    """
    phones = []
    for phone in form.phones.data:
        phone_number = phone.get("value")
        if phone_number:
            phones.append(Phone(value=phone_number))

    emails = []
    for email in form.emails.data:
        email_address = email.get("value")
        if email_address:
            emails.append(Email(value=email_address))
    record.birthday = form.birthday.data
    record.phones = phones
    record.emails = emails
    db.session.commit()


def delete_record_book(book: RecordBook):
    db.session.delete(book)
    db.session.commit()


def delete_record(record: Record):
    db.session.delete(record)
    db.session.commit()

