from datetime import datetime
from typing import List, Union
from uuid import UUID

from sqlalchemy.orm import Session

from api.models.articles import Article
from api.schemas.articles import ArticleBase, ArticleUpdate


class ArticleRepository:

    @staticmethod
    def create_article(*, request_body: ArticleBase, db: Session) -> Article:
        new_article = Article(**request_body.dict())
        db.add(new_article)
        db.commit()
        db.refresh(new_article)  # Now it contains all attrs from created model
        return new_article

    @staticmethod
    def delete_article(*, uuid: UUID, db: Session) -> Union[Article, None]:
        article = ArticleRepository.get_article(uuid=uuid, db=db)
        if article is not None:
            db.delete(article)
            db.commit()
        return article

    @staticmethod
    def get_all_articles(db: Session) -> List[Article]:
        return db.query(Article).all()

    @staticmethod
    def get_article(*, uuid: UUID, db: Session) -> Union[Article, None]:
        return db.query(Article).filter_by(uuid=uuid).first()

    @staticmethod
    def update_article(*, uuid: UUID, request_body: ArticleUpdate, db: Session) -> Union[Article, None]:
        article = ArticleRepository.get_article(uuid=uuid, db=db)
        request_data = request_body.dict()
        for field in request_data:
            value = request_data[field]
            if value is not None:
                setattr(article, field, value)  # updating field if it was given in request

        article.edited_at = datetime.utcnow()  # updating edited time
        db.commit()

        return article
