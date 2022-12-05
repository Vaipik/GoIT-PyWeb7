from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    record_book = db.relationship("RecordBook", back_populates="user", cascade="all, delete-orphan")
    note_book = db.relationship("NoteBook", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class RecordBook(db.Model):
    __tablename__ = "record_books"

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), index=True, nullable=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="record_book")
    record = db.relationship("Record", back_populates="book", cascade="all, delete-orphan")


class NoteBook(db.Model):
    __tablename__ = "note_books"

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), index=True, nullable=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="note_book")


class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    birthday = db.Column(db.Date, default=None, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("record_books.id"))
    book = db.relationship("RecordBook", back_populates="record")
    phones = db.relationship("Phone", back_populates="record")
    emails = db.relationship("Email", back_populates="record")


class Phone(db.Model):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), index=True, nullable=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"))
    record = db.relationship("Record", back_populates="phones")


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), index=True, nullable=True)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"))
    record = db.relationship("Record", back_populates="emails")


@login.user_loader
def load_user(id: str):
    return User.query.get(int(id))
