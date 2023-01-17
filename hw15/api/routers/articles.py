from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependecies import get_db
from api.repositories.articles import ArticleRepository
from api.schemas.articles import ArticleBase, ArticleResponse, ArticleUpdate, Article404, Articles404


router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.post(
    path="/",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_article(article: ArticleBase, db: Session = Depends(get_db)):
    new_article = ArticleRepository.create_article(
        request_body=article,
        db=db
    )
    return new_article


@router.delete(
    path="/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Article404}
    }
)
def delete_article(uuid: UUID, db: Session = Depends(get_db)):
    deleted_article = ArticleRepository.delete_article(
        uuid=uuid,
        db=db
    )
    if deleted_article is None:
        return JSONResponse(
            content={
                "uuid": str(uuid),
            },
            status_code=status.HTTP_404_NOT_FOUND
        )
    return deleted_article


@router.get(
    path="/",
    response_model=List[ArticleResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Articles404}
    }
)
def get_all_articles(db: Session = Depends(get_db)):
    articles = ArticleRepository.get_all_articles(db)
    if articles is None:
        return JSONResponse(
            content={"mesage": "No articles were found"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return articles


@router.get(
    path="/{uuid}",
    response_model=ArticleResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Article404}
    }
)
def get_article(uuid: UUID, db: Session = Depends(get_db)):
    article = ArticleRepository.get_article(uuid=uuid, db=db)
    if article is None:
        return JSONResponse(
            content={
                "uuid": str(uuid),
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return article


@router.put(
    path="/{uuid}",
    response_model=ArticleResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Article404}
    }
)
def update_article(uuid: UUID, article: ArticleUpdate, db: Session = Depends(get_db)):
    article = ArticleRepository.update_article(
        uuid=uuid,
        request_body=article,
        db=db
    )
    if article is None:
        return JSONResponse(
            content={
                "uuid": str(uuid),
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return article
