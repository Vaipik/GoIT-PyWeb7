import csv
import pathlib

from src.repository.currency import CurrencyCRUD


async def get_codes(session) -> list[dict]:
    """
    Taking data from csv file and returns dictionary with key as currency code according to ISO4217 and value as
    currency name.\n
    :return: list with dictionaries [k: int = CurrencyCode, value: str =CurrencyName]
    """
    BASE_DIR = pathlib.Path(__file__).parent
    data_file_path = BASE_DIR / "data" / "codes.csv"

    with open(data_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        codes_list = []
        for cur in reader:
            if cur["code"]:
                existance = await CurrencyCRUD.get_currency_name(session, int(cur["code"]))
                if not existance:
                    cur["code"] = int(cur.get("code"))
                    codes_list.append(cur)

    return codes_list

