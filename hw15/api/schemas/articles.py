from datetime import datetime, timedelta
from typing import Optional, Union
from uuid import UUID


from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    title: str = Field(example="How to create api ?")
    text: str = Field(example="Here must be article text, but it can be very large so...")


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(example="How to create api ?")
    text: Optional[str] = Field(example="Here must be article text, but it can be very large so...")


class ArticleResponse(ArticleBase):
    uuid: UUID
    created_at: datetime = Field(example=(datetime.utcnow() - timedelta(days=30)))
    edited_at: Union[datetime, None] = Field(example=datetime.utcnow())

    class Config:
        orm_mode = True


# Error schemas

class Articles404(BaseModel):
    message: str


class Article404(BaseModel):
    uuid: UUID
    message = "Article with given uuid was not found"
