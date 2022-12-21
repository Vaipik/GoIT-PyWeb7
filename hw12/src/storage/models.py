from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.libs import constants


Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    country = Column(String(constants.COUNTRY_LENGTH))
    currency = Column(String(constants.CURRENCY_FULLNAME_LENGTH))
    name = Column(String(constants.CURRENCY_SHORTNAME_LENGTH))
    code = Column(Integer)
    minor = Column(String(constants.MINOR_LENGTH))


class MonoBank(Base):
    __tablename__ = "monobank"

    id = Column(Integer, primary_key=True)

    currency = Column(String(constants.CURRENCY_SHORTNAME_LENGTH))
    rate_sell = Column(Float)
    rate_buy = Column(Float)
    date = Column(Date)


async def async_pg_context(app):

    conf = app['config']['postgres']
    url_db = f"postgresql+asyncpg://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
    engine = create_async_engine(url_db)
    DBSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    session = DBSession()
    app['db_session'] = session
    yield
    app['db_session'].close()
