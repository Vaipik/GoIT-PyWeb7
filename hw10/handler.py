from __future__ import annotations

import re
from datetime import datetime, timedelta

from database.models import Email, Phone, Record, Note, Tag
import database.connect
from error_handler import error_handler


@error_handler
def add_birthday(*args) -> None:  # username birthday
    """
    Is used to add or change contact birthday.\n
    :param args: username birthday.
    :return: None
    """
    name, birthday, *tail = args
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    Record.objects(name=name).update(birthday=birthday)


@error_handler
def add_email(*args) -> None:  # username email
    """
    Is used to add new email to record.\n
    :param args: username email.
    :return: None
    """
    name, email, *tail = args
    Record.objects(name=name).update_one(push__emails=Email(email_address=email).save())


@error_handler
def add_phone(*args) -> None:
    """
    Is used to add new phone to contact record.\n
    :param args: username phone
    :return: None
    """
    name, phone, *tail = args
    Record.objects(name=name).update_one(push__phones=Phone(phone_number=phone).save())


@error_handler
def birthdays_in(*args) -> None:  # days
    """
    Show birthday persons in given days.\n
    :param args: days
    :return: None
    """
    days = int(args[0]) if args else 30
    records = Record.objects(birthday__ne=None)
    today_date = datetime.today().date()
    birthdays = []
    for record in records:
        this_year_bday: datetime = record.birthday.replace(year=datetime.today().year)
        if today_date == this_year_bday:
            birthdays.append(
                f"{record.name} has birthday today!"
            )
        elif today_date < this_year_bday <= today_date + timedelta(days):
            birthdays.append(
                f"{record.name} has birthday in {(this_year_bday - today_date).days}! days"
            )

    if birthdays:
        print(*birthdays, sep="\n")
    else:
        print(f"No birthday persons in your contacts for {days} days")


@error_handler
def check_tag(tag: str) -> Tag | None:
    """
    Is used to check tag existence in db.\n
    :param tag: tag name
    :return: Tag or None if tag does not exist
    """
    return Tag.objects(tag_name=tag)


@error_handler
def delete_birthday(*args) -> None:  # username
    """
    Is used to delete contact birthday
    :param args: Username
    :return: None
    """
    name, *tail = args
    Record.objects(name=name).update(birthday=None)


@error_handler
def delete_contact(*args) -> None:
    """
    Deleting contact record.\n
    :param args: contact name.
    :return: None
    """
    name, *tail = args
    Record.objects(name=name).delete()


@error_handler
def delete_email(*args) -> None:  # username email
    """
    Is used to delete email from contact record.\n
    :param args: username email.
    :return: None
    """
    name, email_to_delete, *tail = args
    record: Record = Record.objects(name=name).get()
    for email in record.emails:
        if email_to_delete == email.email_address:
            record.emails.remove(email)
            email.delete()

    record.update(emails=record.emails)


@error_handler
def delete_phone(*args) -> None:
    """
    Is used to change contact phone.\n
    :param args: Username phone
    :return: None
    """
    name, phone_to_delete, *tail = args
    record: Record = Record.objects(name=name).get()
    for phone in record.phones:
        if phone_to_delete == phone.phone_number:
            record.phones.remove(phone)
            phone.delete()

    record.update(phones=record.phones)


@error_handler
def delete_note(*args) -> None:
    """
    Is used to delete note.\n
    :param args: note title
    :return: None
    """
    title, *tail = args
    Note.objects(title=title).delete()


@error_handler
def delete_tag(*args) -> None:
    """
    Deleting tag from db.\n
    :param args: tag name.
    :return: None
    """
    tag, *tail = args
    Tag.objects(tag_name=tag).delete()


@error_handler
def edit_note(*args) -> None:
    """
    Editing note title or text.\n
    :param args: note title to be edited
    :return: None
    """
    title, *tail = args

    note: Note = Note.objects(title=title).get()
    print(note)

    edit_title = input(">>> Would you like to edit note title: [y/n]").strip()
    if edit_title == "y":
        new_title = input(">>> Enter new title: ").strip()
        note.update(title=new_title)

    edit_text = input(">>> Would you like to change note text: [y/n]")
    if edit_text == "y":
        new_text = input(">>> Enter new note text: ").strip()
        note.update(text=new_text)

    edit_tag = input(">>> Would you like to change note tag: [y/n]")
    if edit_tag == "y":
        new_tag = input(">>> Enter new note text: ").strip()
        checked = check_tag(new_tag)
        new_tag = Tag(tag_name=new_tag).save() if checked is None else checked.get()
        note.update(tag=new_tag)
    if "y" in (edit_title, edit_text, edit_tag):
        note.update(edited_at=datetime.now())


@error_handler
def find_record(*args) -> None:
    """
    Finding record by checking bday, name, phones or email.
    :param args: something to be found
    :return:
    """
    query, *tail = args
    for record in Record.objects:
        phones = []
        emails = []
        birthday = None
        name = None

        if query.isdigit():
            for phone in record.phones:
                print(phone.phone_number)
                if query in phone.phone_number:
                    phones.append(phone)

            if query in record.birthday.strftime("%Y-%m-%d"):
                birthday = record.birthday

        elif "@" in query:
            for email in record.emails:
                if query in email.email_address:
                    emails.append(email)
        elif query in record.name:
            name = record.name

        if any([phones, emails, birthday, name]):
            print("You are looking for:")
            print(name if name else record.name)
            print(birthday)
            print(*phones)
            print(*emails)


@error_handler
def find_note(*args) -> None:
    """
    Is used to find note by title or text
    :param args:
    :return:
    """
    query, *tail = args
    notes = Note.objects

    for note in notes:
        flag = True if query in note.title or query in note.text else False
        if flag:
            print(f"Title: {note.title}")
            print(f"Text [limited to 50 symbols]: {note.text[:50]}")


@error_handler
def get_record(*args) -> None:
    """
    Getting one contact.\n
    :param args: contact name.
    :return: None
    """
    name, *tail = args
    record = Record.objects(name=name)
    print(record)


@error_handler
def get_note(*args) -> None:
    """
    Getting one note.\n
    :param args: note title.
    :return: None
    """
    title, *tail = args
    note = Note.objects(title=title)
    print(note)


@error_handler
def new_contact(*args) -> None:
    """
    Adding new contact.\n
    :param args: query
    :return: None
    """
    name, *tail = args
    record = Record(name=name).save()
    phones = []
    emails = []
    birthday = None

    for item in tail:

        if item.isdigit():
            phones.append(Phone(phone_number=item, record=record).save())

        elif '@' in item:
            emails.append(Email(email_address=item, record=record).save())

        elif birthday is None:
            date = re.match(r"^\d{4}-\d{2}-\d{2}$", item).group()
            birthday = datetime.strptime(date, "%Y-%m-%d").date() if date else None

    record.update(
        birthday=birthday,
        emails=emails,
        phones=phones
    )


@error_handler
def new_note(*args) -> None:  # title text tag
    """
    Adding new note to notebook.\n
    :param args: title is must have parameter
    :return: None
    """
    title, *tail = args
    checked_title = Note.objects(title=title)
    if checked_title:
        print(f"{title}'s record already exists")
        return

    is_tag = input(">>> Would you like to add a tag ? [y/n]: ").strip()
    tag = input(">>> Add your tag: ").strip() if is_tag == "y" else None
    text = input(">>> Enter note text if needed: ").strip()
    if tag is not None:
        checked_tag = check_tag(tag)
        tag = Tag(tag_name=tag).save() if not checked_tag else checked_tag.get()

    Note(
        title=title,
        text=text,
        tag=tag,
    ).save()


def show_help(*args):
    print("I can operate your phonebook and your notebook.\nPhonebook actions:")
    print("> add <birthday, email, phone> <username> <birthday data> to add new data to existing contact.")
    print("> birthdays in <days> to find users who has birthday in given gap. Days is not obligatory")
    print("> delete <<birthday, email, phone> <username> <data> to delete desired data.\n"
          "  In case of birthday it is not necessary to enter data")
    print("> delete contact <username> to delete record from your phonebook")
    print("> edit <birthday, email, phone> <username> <old_data> <new_data> to change desired data")
    print("> find phonebook <any data> to search in your contacts")
    print("> new contact <username> <any data>. Data must be separated by spaces.\n"
          "  Data is not necessary and can be phone(s), email(s) and birthday.")
    print("> show contact <username> to show contact data")
    print("> show contacts <records per page> to show your phonebook contacts.\n"
          "  records per page is not necessary parameter")
    print("Notebook actions:")
    print("> new note <title> to start adding note.")
    print("> edit note <title> to start editing note")
    print("> find note <query> to start search in your notebook")
    print("> show note <title> to exact note.")
    print("> show notes to show all titles\n")
    print("> show help to see again what can i do :)")


@error_handler
def show_records(*args) -> None:
    """
    Showing all contacts.\n
    :return: None
    """
    records = Record.objects
    for record in records:
        print(record.name)


@error_handler
def show_notes(*args) -> None:
    """
    Showing all notes.\n
    :return: None
    """
    notes = Note.objects
    for note in notes:
        print(note.title)


OPERATIONS = {
    'add birthday': add_birthday,
    'add email': add_email,
    'add phone': add_phone,
    'birthdays in': birthdays_in,
    'delete birthday': delete_birthday,
    'delete contact': delete_contact,
    'delete email': delete_email,
    'delete phone': delete_phone,
    'delete note': delete_note,
    'edit birthday': add_birthday,
    'edit note': edit_note,
    'find note': find_note,
    'find phonebook': find_record,
    'new contact': new_contact,
    'new note': new_note,
    'show contact': get_record,
    'show contacts': show_records,
    'show help': show_help,
    'show note': get_note,
    'show notes': show_notes,
}


def suitable_command(input_command: str) -> str:
    """
    Recursive function which is trying to find correct command in case of wrong command.\n
    :param input_command: command to be found on
    :return: the best suitable command
    """
    for command in OPERATIONS. keys():
        if input_command in command:
            return command
    return suitable_command(input_command[:-1])


def wrong_command(*args):
    """
    Show more suitable command in it was wrong.\n
    :param args: command action
    :return: None
    """
    input_command = f"{args[0]} {args[1]}"
    print(f"Maybe you mean {suitable_command(input_command)}")


def input_parser(user_input: str) -> list:
    """
    Is used to parse user input.\n
    :param user_input: input string
    :return: list with query
    """
    stop_word = ('stop', 'exit', 'goodbye')
    for word in stop_word:
        if word in user_input.lower():
            return ['break', []]

    user_input = user_input.split()
    return ['wrong', 'command'] if len(user_input) < 2 else user_input


@error_handler
def run():
    """
    Handler function which is accumulating all operations with phonebook, notebook.\n
    :params: None
    :return: None
    """

    print('>>> Greetings! I am your CLI helper. Enter show help to see what can i do.'
          '\n>>> Or try yourself :)')
    while True:
        command, data_type, *query = input_parser(input('<<< Enter your command: '))
        if command == 'break':
            print('\nGoodbye! I will be waiting for you comeback :)')
            break

        action = OPERATIONS.get(command + ' ' + data_type, wrong_command)
        if action.__name__ == 'wrong_command':
            action(command, data_type)

        else:

            if not query:
                query = []

            action(*query)


if __name__ == "__main__":
    run()
