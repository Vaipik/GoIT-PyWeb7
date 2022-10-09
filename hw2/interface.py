from abc import ABC, abstractmethod
from collections import UserDict

from phonebook import AddressBook


class IConsole(ABC):

    @abstractmethod
    def print_to_console(self, cls_instance, data):
        """
        Show data from given class.\n
        :param data: to be shown
        :param cls_instance: class instance
        """
        pass


class PrintRecord(IConsole):

    def print_to_console(self, cls_instance: AddressBook, data: str):
        """
        Show fields from record on page.\n
        :param data: contact name
        :param cls_instance: AddressBook instance
        """
        record = cls_instance.show_record_data(data)
        for field in record:
            print(*field)


class PrintPhoneBook(IConsole):

    def print_to_console(self, cls_instance: AddressBook, data: str):
        """
        Show fields from records on page.\n
        :param data: number of fields shown on one page
        :param cls_instance: AddressBook instance
        """
        pages = cls_instance.show_contacts(int(data)) if int(data) else cls_instance.show_contacts()
        for page in pages:
            for data in page:
                print(*data)


class PrintBirthdays(IConsole):

    def print_to_console(self, cls_instance, data):
        """
        Show birthdays in given days.\n
        :param data: days gap
        :param cls_instance: AddressBook instance
        """
        days = int(data) if data else None
        birthdays = cls_instance.show_near_birthdays(days) if days else cls_instance.show_near_birthdays()
        print(*birthdays, sep='\n')


class PrintPhoneBookSearch(IConsole):

    def print_to_console(self, cls_instance, data: str):
        """
        Show similar records data according to given query.\n
        :param data: given query
        :param cls_instance: AddressBook instance
        """
        information = cls_instance.find_record(data)
        for answer in information:

            for username, fields in answer.items():

                if len(fields) == 1 and username == fields[0]:  # username is a key
                    print(f"Looks like you are looking for {username} contact")
                else:
                    print(f"Looks like you are looking for {username} data:")
                    for field in fields:
                        print(field[0], end=': ')
                        print(*field[1:], sep=', ')
