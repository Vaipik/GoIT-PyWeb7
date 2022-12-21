from datetime import datetime

from sqlalchemy import select, and_

from src.storage.models import MonoBank


class MonoBankCRUD:

    @staticmethod
    async def write_to_db(session, data: list[dict]):
        for currency in data:
            existance = await MonoBankCRUD.check_existance(session, currency)
            if not existance:
                session.add(MonoBank(**currency))
        await session.commit()

    @staticmethod
    async def check_existance(session, data: dict):

        currency, date = data["currency"], data["date"]
        result = await session.execute(
            select(MonoBank.currency).where(and_(MonoBank.date == date, MonoBank.currency == currency))
        )
        return result.scalars().all()

    @staticmethod
    async def get_currencies_rates(session, date: datetime):

        currencies = await session.execute(
            select(MonoBank).where(MonoBank.date == date)
        )

        return currencies.scalars().all()
