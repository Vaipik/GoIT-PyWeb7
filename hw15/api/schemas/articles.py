from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    title: str = Field("How to create api ?")
    text: str = Field("Here must be article text, but it can be very large so...")


class ArticleUpdate(ArticleBase):
    uuid: UUID


class ArticleDelete(BaseModel):
    uuid: UUID
    title: str


class ArticleResponse(ArticleBase):
    uuid: UUID
    created_at: datetime = (datetime.utcnow() - timedelta(days=30)).timestamp()
    edited_at: datetime = datetime.utcnow().timestamp()

    class Config:
        orm_mode = True
