from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TEXT

from api.db.database import Base
from api.libs import constants


class Article(Base):
    __tablename__ = "articles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(length=constants.ARTICLE_TITLE_MAX_LENGTH))
    text = Column(TEXT)
    created_at = Column(TIMESTAMP, default=datetime.utcnow().timestamp)
    added_at = Column(TIMESTAMP, default=None)


