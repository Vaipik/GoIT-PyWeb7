from sqlalchemy import select

from src.storage.models import Currency


class CurrencyCRUD:

    @staticmethod
    async def get_currency_name(session, code: int):
        result = await session.execute(select(Currency.name).where(Currency.code == code))
        return result.scalars().first()

    @staticmethod
    async def write_to_db(session, codes_list):
        [session.add(Currency(**currency)) for currency in codes_list]
        await session.commit()
