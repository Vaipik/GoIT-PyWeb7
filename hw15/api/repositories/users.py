from typing import Union

from sqlalchemy.orm import Session

from ..schemas.users import UserBase
from ..models.users import User
from ..libs.hash import Hash


class UserRepository:

    @staticmethod
    def get_user(*, username: str, db: Session) -> Union[User, None]:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def create_user(*, user: UserBase, db: Session) -> User:
        username, password = user.username, user.password
        user = User(
            username=username,
            hashed_password=Hash.get_password_hash(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)  # Update attributes from db
        return user

