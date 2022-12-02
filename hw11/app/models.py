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


class NoteBook(db.Model):
    __tablename__ = "note_books"

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), index=True, nullable=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="note_book")


@login.user_loader
def load_user(id: str):
    return User.query.get(int(id))
