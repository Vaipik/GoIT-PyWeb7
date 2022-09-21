"""
Напишіть класи серіалізації контейнерів з даними Python у json, bin файли.
Самі класи мають відповідати загальному інтерфейсу (абстрактному базовому класу) SerializationInterface.
"""
from abc import ABCMeta, abstractmethod
import json
from pathlib import Path
import pickle


class SerializationInterface(metaclass=ABCMeta):

    @abstracthmethod
    def serialize(self, filename, data):
        pass

    @abstractmethod
    def deserialize(self, filename):
        pass


class SerializationListJSON(SerializationInterface):

    def serialize(self, filename: Path, data: list) -> None:

        if not isinstance(data, list):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> list:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)


class SerializationTupleJSON(SerializationInterface):

    def serialize(self, filename: Path, data: tuple) -> None:

        if not isinstance(data, tuple):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> tuple:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise TypeError(f'Wrong data in {filename}')

            return tuple(json.load(file))


class SerializationDictJSON(SerializationInterface):

    def serialize(self, filename: Path, data: dict) -> None:

        if not isinstance(data, dict):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> dict:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, dict):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)


class SerializationListBIN(SerializationInterface):

    def serialize(self, filename: Path, data: list) -> None:

        if not isinstance(data, list):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> list:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)


class SerializationTupleBIN(SerializationInterface):

    def serialize(self, filename: Path, data: tuple) -> None:

        if not isinstance(data, tuple):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> tuple:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, tuple):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)


class SerializationSetBIN(SerializationInterface):

    def serialize(self, filename: Path, data: set) -> None:

        if not isinstance(data, set):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> set:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, set):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)


class SerializationDictBIN(SerializationInterface):

    def serialize(self, filename: Path, data: dict) -> None:

        if not isinstance(data, dict):
            raise TypeError('Wrong datatype')

        with open(filename, 'w') as file:
            json.dump(data, file)

    def deserialize(self, filename: Path) -> dict:

        with open(filename) as file:
            data = json.load(file)

            if not isinstance(data, dict):
                raise TypeError(f'Wrong data in {filename}')

            return json.load(file)
