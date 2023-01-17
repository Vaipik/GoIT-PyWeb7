from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.dependecies import get_db
from api.repositories.articles import ArticleRepository
from api.schemas.articles import ArticleBase, ArticleResponse, ArticleUpdate

router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.post("/", response_model=ArticleResponse)
def create_article(article: ArticleBase, db: Session = Depends(get_db)):
    new_article = ArticleRepository.create_article(
        request_body=article,
        db=db
    )
    return new_article


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(uuid: UUID, db: Session = Depends(get_db)):
    deleted_article = ArticleRepository.delete_article(
        uuid=uuid,
        db=db
    )
    if deleted_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No article was found"
        )
    return deleted_article


@router.get("/", response_model=List[ArticleResponse])
def get_all_articles(db: Session = Depends(get_db)):
    articles = ArticleRepository.get_all_articles(db)
    if articles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No articles were found"
        )
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


@router.put("/{uuid}", response_model=ArticleResponse)
def update_article(uuid: UUID, article: ArticleUpdate, db: Session = Depends(get_db)):
    article = ArticleRepository.update_article(
        uuid=uuid,
        request_body=article,
        db=db
    )
    return article
