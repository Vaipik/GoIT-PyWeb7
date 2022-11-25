from __future__ import annotations
from datetime import datetime
import re

from mongoengine import EmbeddedDocument, Document, CASCADE, NULLIFY
from mongoengine.fields import DateField, DateTimeField, StringField, ListField, ReferenceField, EmbeddedDocumentField


def _correct_email(email):
    pattern = r"^[a-zA-Z][\w.]+@([a-zA-Z]{2,}[.][a-zA-Z]{2,}|[a-zA-Z]{2,}[.][a-zA-Z]{2,}[.][a-zA-Z]{2,})$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email address")


def _correct_phone(phone_number):
    if not phone_number.isdigit():
        raise ValueError("Invalid phone number")


class Record(Document):
    name = StringField(max_length=100, required=True, unique=True)
    birthday = DateField(default=None)
    phones = ListField(ReferenceField("Phone"))
    emails = ListField(ReferenceField("Email"))

    meta = {
        "ordering": ["+name"]
    }

    @staticmethod
    def _unpacked_list(field: list):
        items_per_field = len(field)
        template = "{}, " * items_per_field
        return template.format(*field)[:-2]

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Birthday: {self.birthday if self.birthday else 'No data'}\n" \
               f"Phones: {self._unpacked_list(self.phones) if self.phones else 'No data'}\n" \
               f"Emails: {self._unpacked_list(self.emails) if self.emails else 'No data'}"

    def __repr__(self):
        return self.__str__()


class Phone(Document):
    phone_number = StringField(max_length=30, unique=True, validation=_correct_phone)
    record = ReferenceField(Record, reverse_delete_rule=CASCADE)

    def __str__(self):
        return self.phone_number

    def __repr__(self):
        return self.__str__()


class Email(Document):
    email_address = StringField(max_length=50, validation=_correct_email)
    record = ReferenceField(Record, reverse_delete_rule=CASCADE)

    def __str__(self):
        return self.email_address

    def __repr__(self):
        return self.__str__()


class Tag(Document):
    tag_name = StringField(max_length=100, unique=True)
    notes = ListField(ReferenceField("Note"))

    def __str__(self):
        return self.tag_name

    def __repr__(self):
        return self.__str__()


class Note(Document):
    title = StringField(max_length=100, required=True, unique=True)
    text = StringField(max_length=255, required=False)
    created_at = DateTimeField(default=datetime.now())
    edited_at = DateTimeField(default=None)
    tag = ReferenceField("Tag", reverse_delete_rule=NULLIFY)

    meta = {
        "ordering": ["+title", "-created_at"]
    }

    def __str__(self):
        return f"Title: {self.title}\n" \
               f"Tags: {self.tag if self.tag else 'No data'}\n" \
               f"Text: {self.text if self.text else 'No text'}\n" \
               f"Created at:  {self.created_at}\t" \
               f"'Edited at: '{self.edited_at if self.edited_at else 'Not edited yet'}"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    Record.objects().get()


