from uuid import uuid4

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from api.database.base_class import Base
from api.libs import constants


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(constants.HASHPASSWORD_MAX_LENGTH), nullable=False, unique=True)
    hashed_password = Column(String(constants.HASHPASSWORD_MAX_LENGTH), nullable=False)
    is_active = Column(Boolean, default=True)
    last_logged = Column(TIMESTAMP, nullable=True, default=None)
