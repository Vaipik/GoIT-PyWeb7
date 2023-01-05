from sqlalchemy import Column, Integer, String

from src.storage.db import Base


class Advertisment(Base):
    __tablename__ = "puppies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    price = Column(Integer)
    location = Column(String(255))
    url = Column(String(255), unique=True)
