from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config import config


SQLALCHEMY_DATABASE_URL = config.app_config["DB_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
