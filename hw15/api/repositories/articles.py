from datetime import datetime
from typing import List, Union
from uuid import UUID

from sqlalchemy.orm import Session

from api.models.articles import Article
from api.schemas.articles import ArticleBase, ArticleUpdate


class ArticleRepository:

    @staticmethod
    def create_article(*, request_body: ArticleBase, db: Session) -> Article:
        """
        Creating new article, returns created instance
        :param request_body: body parameters according to json schema
        :param db: session instance
        :return: Created article instance
        """
        new_article = Article(**request_body.dict())
        db.add(new_article)
        db.commit()
        db.refresh(new_article)  # Now it contains all attrs from created model
        return new_article

    @staticmethod
    def delete_article(*, uuid: UUID, db: Session) -> Union[Article, None]:
        """
        Delete existing article by uuid if it exists
        :param uuid: universaly unique identifier
        :param db: session instance
        :return: Article if it exists or None
        """
        article = ArticleRepository.get_article(uuid=uuid, db=db)
        if article is not None:
            db.delete(article)
            db.commit()
        return article

    @staticmethod
    def get_all_articles(db: Session) -> Union[List[Article], None]:
        """
        Getting all existing articles in db.
        :param db: session instance
        :return: list with all existing articles, None if no articles exist
        """
        articles = db.query(Article).all()
        return articles if articles else None

    @staticmethod
    def get_article(*, uuid: UUID, db: Session) -> Union[Article, None]:
        """
        Getting single article by uuid if it exists
        :param uuid: universally unique identifier
        :param db: session instance
        :return: Article instance or None if no article
        """
        return db.query(Article).filter_by(uuid=uuid).first()

    @staticmethod
    def update_article(*, uuid: UUID, request_body: ArticleUpdate, db: Session) -> Union[Article, None]:
        """
        Updating article if it exists
        :param uuid: universally unique identifier.
        :param request_body: body parameters which will update article fields
        :param db: session instance
        :return: Updated article or None if no article
        """
        article = ArticleRepository.get_article(uuid=uuid, db=db)
        if article is None:
            return article

        request_data = request_body.dict()
        for field in request_data:
            value = request_data[field]
            if value is not None:
                setattr(article, field, value)  # updating field if it was given in request

        article.edited_at = datetime.utcnow()  # updating edited time
        db.commit()

        return article
