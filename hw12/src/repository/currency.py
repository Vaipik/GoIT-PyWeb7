from sqlalchemy import select

from src.storage.models import Currency


class CurrencyCRUD:

    def get_currency_name(self, session, code: int):
        result = session.execute(select(Currency.name).where(Currency.code == str(code)))
        return result

    def write_to_db(self, session, codes_list):
        [session.add(Currency(**currency)) for currency in codes_list]
        session.commit()

