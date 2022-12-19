import csv
import pathlib


def get_codes() -> dict:
    """
    Taking data from csv file and returns dictionary with key as currency code according to ISO4217 and value as
    currency name.\n
    :return: list with dictionaries [k: int = CurrencyCode, value: str =CurrencyName]
    """
    BASE_DIR = pathlib.Path(__file__).parent
    data_file_path = BASE_DIR / "data" / "codes.csv"

    with open(data_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        lst = [currency for currency in reader]

    return lst

