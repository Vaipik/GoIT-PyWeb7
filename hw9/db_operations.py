from datetime import datetime, timedelta
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from error_handler import error_handler
from models import Record, Phone, Email, Note, Tag, Base


@error_handler
def add_birthday(*args, session) -> None:  # username birthday
    """
    Is used to add or change contact birthday.\n
    :param args: username birthday.
    :param session: current session instance.
    :return: None
    """
    name, birthday, *tail = args
    birthday = datetime.strptime(birthday, "%Y-%m-%d")

    session.query(Record).filter_by(name=name).update(
        {"birthday": birthday}, synchronize_session="fetch"
    )


@error_handler
def add_email(*args, session) -> None:  # username email
    """
    Is used to add new email to record.\n
    :param args: username email.
    :param session: current session instance.
    :return: None
    """
    name, email, *tail = args
    contact: Record = session.query(Record).filter_by(name=name).one()
    contact.emails.append(Email(email_address=email))


@error_handler
def add_phone(*args, session) -> None:
    """
    Is used to add new phone to contact record.\n
    :param args: username phone
    :param session: current session instance.
    :return: None
    """
    name, phone, *tail = args
    contact: Record = session.query(Record).filter_by(name=name).one()
    contact.phones.append(Phone(phone_number=phone))


@error_handler
def birthdays_in(*args, session) -> None:  # days
    """
    Show birthday persons in given days.\n
    :param args: days
    :param session: current session instance.
    :return: None
    """
    days = int(args[0]) if args else 30
    records = session.query(Record).order_by("name")
    today_date = datetime.today().date()
    birthdays = []
    for record in records:
        if record.birthday is None:
            continue

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
def check_tag(tag: str, session) -> Tag | None:
    """
    Is used to check tag existence in db.\n
    :param tag: tag name
    :param session: current session
    :return: Tag or None if tag does not exist
    """
    result = session.query(Tag).filter_by(tag_name=tag)
    return result.one_or_none()


@error_handler
def delete_birthday(*args, session) -> None:  # username
    """
    Is used to delete contact birthday
    :param args: Username
    :param session: current session instance.
    :return: None
    """
    name, *tail = args
    birthday = None

    session.query(Record).filter_by(name=name).update(
        {"birthday": birthday}, synchronize_session="fetch"
    )


@error_handler
def delete_contact(*args, session) -> None:
    """
    Deleting contact record.\n
    :param args: contact name.
    :param session: current session instance.
    :return: None
    """
    name, *tail = args
    contact_to_delete = session.query(Record).filter_by(name=name).one()
    session.delete(contact_to_delete)


@error_handler
def delete_email(*args, session) -> None:  # username email
    """
    Is used to delete email from contact record.\n
    :param args: username email.
    :param session: current session instance.
    :return: None
    """
    name, email_to_delete, *tail = args
    contact: Record = session.query(Record).filter_by(name=name).one()
    for email in contact.emails:
        if email_to_delete == email.email_address:
            print(email)
            contact.emails.remove(email)
            break


@error_handler
def delete_phone(*args, session) -> None:
    """
    Is used to change contact phone.\n
    :param args: Username phone
    :param session: current session instance.
    :return: None
    """
    name, phone_to_delete, *tail = args
    contact: Record = session.query(Record).filter_by(name=name).one()
    for phone in contact.phones:
        if phone_to_delete == phone.phone_number:
            contact.phones.remove(phone)
            break


@error_handler
def delete_note(*args, session) -> None:
    """
    Is used to delete note.\n
    :param args: note title
    :param session: current session instance.
    :return: None
    """
    title, *tail = args
    note_to_delete = session.query(Note).filter_by(title=title).one()
    session.delete(note_to_delete)


@error_handler
def delete_tag(*args, session) -> None:
    """
    Deleting tag from db.\n
    :param args: tag name.
    :param session: current session instance.
    :return: None
    """
    tag, *tail = args
    tag_to_delete = session.query(Tag).filter_by(tag_name=tag).one()
    session.delete(tag_to_delete)


@error_handler
def edit_note(*args, session) -> None:
    """
    Editing note title or text.\n
    :param args: note title to be edited
    :param session: current session instance.
    :return: None
    """
    title, *tail = args

    note = session.query(Note).filter_by(title=title).one()
    print(note)

    edit_title = input(">>> Would you like to edit note title: [y/n]").strip()
    if edit_title == "y":
        new_title = input(">>> Enter new title: ").strip()
        note.title = new_title

    edit_text = input(">>> Would you like to change note text: [y/n]")
    if edit_text == "y":
        new_text = input(">>> Enter new note text: ").strip()
        note.text = new_text

    edit_tag = input(">>> Would you like to change note tag: [y/n]")
    if edit_tag == "y":
        new_tag = input(">>> Enter new note text: ").strip()
        checked = check_tag(new_tag)
        new_tag = Tag(tag_name=new_tag) if checked is None else checked
        note.tag = new_tag
    if "y" in (edit_title, edit_text, edit_tag):
        note.edited_at = datetime.now()


@error_handler
def find_record(*args, session) -> None:
    """
    Finding record by checking bday, name, phones or email.
    :param args: something to be found
    :param session: current session instance.
    :return:
    """
    query, *tail = args
    if not query.isdigit():

        names = session.query(Record).filter(Record.name.ilike(f"%{query}%")).order_by(Record.name).all()
        print(*names)
        if names:
            print("Looks like you are looking for following contacts: ")
            for name in names:
                print(name.name)

        emails = session.query(Email).join(Record).filter(Email.email_address.ilike(f"%{query}%")).\
            order_by(Record.name).all()
        if emails:
            print("Looks like you are looking for following email: ")
            for email in emails:
                print(email.record.name, email.email_address, sep=': ')

        if not emails and not names:
            print(f"No data '{query}' was found...")

    else:

        phones = session.query(Phone).join(Record).filter(Phone.phone_number.ilike(f"%{query}%")).\
            order_by(Record.name).all()
        if phones:
            print("Looks like you are looking for following phones: ")
            for phone in phones:
                print(phone.record.name, phone.phone_number, sep=': ')

        birthdays = session.query(Record).filter(Record.birthday.ilike(f"%{query}%")).\
            order_by(Record.name).all()
        if birthdays:
            print("Looks like you are looking for following birthdays: ")
            for birthday in birthdays:
                print(birthday.name, birthday.birthday, sep=': ')

        if not phones and not birthdays:
            print(f"No data '{query}' was found...")


@error_handler
def find_note(*args, session) -> None:
    """
    Is used to find note by title or text
    :param args:
    :param session: current session instance.
    :return:
    """
    query, *tail = args
    notes = session.query(Note).filter(Note.title.ilike(f"%{query}%")).order_by(Note.title).all()

    if notes:
        print("Looks like you are looking for following notes: ")
        for note in notes:
            print(note.title)
    else:
        tags = session.query(Tag).join(Note).filter(Tag.tag_name.ilike(f"%{query}%")).order_by(Tag.tag_name).all()
        if tags:
            print("Looks like you are looking for following tags: ")
            for tag in tags:
                print(tag.tag_name, tag.note.title, sep=': ')

        else:
            print(f"No data '{query}' was found...")


@error_handler
def get_record(*args, session) -> None:
    """
    Getting one contact.\n
    :param args: contact name.
    :param session: current session instance
    :return: None
    """
    name, *tail = args
    record = session.query(Record).filter_by(name=name).one()
    print(record)


@error_handler
def get_note(*args, session) -> None:
    """
    Getting one note.\n
    :param args: note title.
    :param session: current session instance
    :return: None
    """
    title, *tail = args
    note = session.query(Note).filter_by(title=title).one()
    print(note)


@error_handler
def new_contact(*args, session) -> None:
    """
    Adding new contact.\n
    :param args: query
    :param session: current session instance.
    :return: None
    """
    name, *tail = args
    phones = []
    emails = []
    birthday = None
    checked_name = session.query(Record).filter_by(name=name).one_or_none()
    if checked_name is not None:
        print(f"{name}'s record already exists")
        return

    for item in tail:

        if item.isdigit():
            phones.append(Phone(phone_number=item))

        elif '@' in item:
            emails.append(Email(email_address=item))

        elif birthday is None:
            date = re.match(r"^\d{4}-\d{2}-\d{2}$", item).group()
            birthday = datetime.strptime(date, "%Y-%m-%d").date() if date else None

    record = Record(
        name=name,
        birthday=birthday,
        phones=phones,
        emails=emails
    )
    session.add(record)


@error_handler
def new_note(*args, session) -> None:  # title text tag
    """
    Adding new note to notebook.\n
    :param args: title is must have parameter
    :param session: current session instance.
    :return: None
    """
    title, *tail = args
    checked_title = session.query(Note).filter_by(title=title).one_or_none()
    if checked_title is not None:
        print(f"{title}'s record already exists")
        return
    is_tag = input(">>> Would you like to add a tag ? [y/n]: ").strip()
    tag = input(">>> Add your tag: ").strip() if is_tag == "y" else None
    text = input(">>> Enter note text if needed: ").strip()
    if tag is not None:
        checked_tag = check_tag(tag)
        tag = Tag(tag_name=tag) if checked_tag is None else checked_tag

    note = Note(
        title=title,
        text=text,
        tag=tag
    )
    session.add(note)


def pagination(query_result) -> None:

    count = 0  # to simulate pages
    for item in query_result:
        print(*item, end=', ')
        count += 1
        if count == 10:
            print()
            count = 0


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
def show_records(*args, session) -> None:
    """
    Showing all contacts.\n
    :param args: None
    :param session: current session instance.
    :return: None
    """
    records = session.query(Record.name).all()
    pagination(records)


@error_handler
def show_notes(*args, session) -> None:
    """
    Showing all notes.\n
    :param args: None
    :param session: current session instance.
    :return: None
    """
    notes = session.query(Note.title).all()
    pagination(notes)


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
    engine = create_engine("sqlite+pysqlite:///hw9.db")
    DBSession = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

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

            with DBSession() as session:
                action(*query, session=session)
                session.commit()


if __name__ == "__main__":
    run()
