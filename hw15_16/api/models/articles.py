from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT
from sqlalchemy.orm import relationship

from api.database.base_class import Base
from api.libs import constants
from api.models.users import User


class Article(Base):
    __tablename__ = "articles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(length=constants.ARTICLE_TITLE_MAX_LENGTH))
    text = Column(TEXT)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    edited_at = Column(TIMESTAMP, default=None)
    user = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="SET NULL"), nullable=True, default=None)
    owner = relationship(User, back_populates="article")
