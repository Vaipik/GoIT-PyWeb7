from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime
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


async def async_mysql_context(app):

    conf = app['config']['mysql']
    url_db = f"postgresql+asyncpg://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
    DBSession = sessionmaker(bind=create_async_engine(url_db), class_=AsyncSession, expire_on_commit=False)
    session = DBSession()
    app['db_session'] = session
    yield
    app['db_session'].close()
    await app['db_session'].wait_closed()


@dataclass
class Currency:
    country: str
    currency: str
    name: str
    code: str
    minor: str
