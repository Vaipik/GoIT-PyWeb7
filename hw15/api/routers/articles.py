from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.dependecies import get_db
from api.models.articles import Article
from api.repositories.articles import ArticleRepository
from api.schemas.articles import ArticleBase, ArticleResponse


router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.get("/", response_model=List[ArticleResponse])
def get_all_articles(db: Session = Depends(get_db)):
    articles = ArticleRepository.get_all_articles(db)
    return articles


@router.get("/{uuid}", response_model=ArticleResponse)
def get_article(uuid: UUID, db: Session = Depends(get_db)):
    article = ArticleRepository.get_article(uuid=uuid, db=db)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No article with such uuid was found"
        )
    return article


@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleBase):
    pass
