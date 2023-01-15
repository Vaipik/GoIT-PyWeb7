from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from api.schemas.articles import ArticleBase, ArticleResponse
from api.models.articles import Article
router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.get("/", response_model=List[ArticleResponse])
def get_all_articles():
    articles = Article.objects.all()
    return articles


@router.get("/{uuid}", response_model=ArticleResponse)
def get_article(uuid: UUID):
    article = Article.objects.filter_by(uuid=uuid).first()
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No article with such uuid was found"
        )
    return article


@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleBase):
    pass
