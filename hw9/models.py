from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime, CHAR


Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    record_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    phones = relationship("Phone", back_populates="record", cascade="all, delete, delete-orphan", innerjoin=True, lazy="joined")  # a link to field in related model
    emails = relationship("Email", back_populates="record", cascade="all, delete, delete-orphan")

    @staticmethod
    def _unpacked_list(field: list):
        items_per_field = len(field)
        template = "{}, " * items_per_field
        return template.format(*field)[:-2]

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Birthday: {self.birthday if self.birthday else 'No data'}\n" \
               f"Phones: {self._unpacked_list(self.phones) if self.phones else 'No data'}\n" \
               f"Emails: {self._unpacked_list(self.emails) if self.emails else 'No data'}\n"

    def __repr__(self):
        return self.__str__()


class Phone(Base):
    __tablename__ = "phones"

    phone_id = Column(Integer, primary_key=True)
    phone_number = Column(CHAR(10), unique=True)
    record_id = Column(Integer, ForeignKey("records.record_id", ondelete="CASCADE", onupdate="CASCADE"))
    record = relationship(Record, back_populates="phones", order_by=Record.name)

    def __repr__(self):
        return f"{self.record.name}: {self.phone_number}"


class Email(Base):
    __tablename__ = "emails"

    email_id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=True)
    record_id = Column(Integer, ForeignKey("records.record_id", ondelete="CASCADE", onupdate="CASCADE"))
    record = relationship("Record", back_populates="emails", order_by=Record.name)

    def __repr__(self):
        return f"{self.email_address}"


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    text = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    edited_at = Column(DateTime, nullable=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    tag = relationship("Tag", back_populates="note")

    def __str__(self):
        return f"Title: {self.title}\n" \
               f"Tag: {self.tag.tag_name if self.tag else 'No tag'}\n" \
               f"Text: {self.text if self.text else 'No text'}\n" \
               f"Created at:  {self.created_at}\t" \
               f"'Edited at: '{self.edited_at if self.edited_at else 'Not edited yet'}"


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(30), unique=True, nullable=False)
    note = relationship("Note", back_populates="tag")
