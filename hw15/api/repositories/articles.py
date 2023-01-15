from typing import List, Union
from uuid import UUID

from sqlalchemy.orm import Session

from api.models.articles import Article
from api.schemas.articles import ArticleBase, ArticleResponse


class ArticleRepository:

    @staticmethod
    def create_article(*, request_body: ArticleBase, db: Session) -> ArticleResponse:
        new_article = Article(
            title=request_body.title,
            text=request_body.text,
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article

    @staticmethod
    def get_all_articles(db: Session) -> List[Article]:
        return db.query(Article).all()

    @staticmethod
    def get_article(*, uuid: UUID, db: Session) -> Union[Article, None]:
        return db.query(Article).filter_by(uuid=uuid).first()

