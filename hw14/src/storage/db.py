from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url = "sqlite+pysqlite:///hw14.db"

Base = declarative_base()
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)
session = DBSession()
