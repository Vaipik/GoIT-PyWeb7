from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    record_book = db.relationship("RecordBook", back_populates="user", cascade="all, delete, delete-orphan")
    note_book = db.relationship("NoteBook", back_populates="user", cascade="all, delete, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class RecordBook(db.Model):
    __tablename__ = "record_books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, nullable=False, unique=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    user = db.relationship("User", back_populates="record_book")
    record = db.relationship("Record", back_populates="book", cascade="all, delete, delete-orphan")


class NoteBook(db.Model):
    __tablename__ = "note_books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, nullable=False, unique=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="note_book")
    note = db.relationship("Note", back_populates="book", cascade="all, delete, delete-orphan")


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    birthday = db.Column(db.Date, default=None, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("record_books.id", ondelete="CASCADE", onupdate="CASCADE"))
    book = db.relationship("RecordBook", back_populates="record")
    phones = db.relationship("Phone", back_populates="record", cascade="all, delete, delete-orphan")
    emails = db.relationship("Email", back_populates="record", cascade="all, delete, delete-orphan")


class Phone(db.Model):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50), index=True, nullable=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id", ondelete="CASCADE", onupdate="CASCADE"))
    record = db.relationship("Record", back_populates="phones")


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(50), index=True, nullable=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id", ondelete="CASCADE", onupdate="CASCADE"))
    record = db.relationship("Record", back_populates="emails", order_by=value)


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(100), index=True, nullable=False)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime, nullable=False, default=None)
    book_id = db.Column(db.Integer, db.ForeignKey("note_books.id", ondelete="CASCADE", onupdate="CASCADE"))
    book = db.relationship("NoteBook", back_populates="note")
    tags = db.relationship("Tag", secondary="note_tags", back_populates="notes")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    notes = db.relationship("Note", secondary="note_tags", back_populates="tags")


class NoteTags(db.Model):
    """
    m2m table for adding multiply tags for one note
    """
    __tablename__ = "note_tags"
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id", ondelete="CASCADE"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id", ondelete="CASCADE"))


@login.user_loader
def load_user(id: str):
    return User.query.get(int(id))
