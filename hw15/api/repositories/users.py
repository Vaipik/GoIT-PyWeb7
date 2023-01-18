from datetime import datetime
from typing import Union

from sqlalchemy.orm import Session

from ..schemas.users import UserBase
from ..models.users import User
from ..libs.hash import Hash


class UserRepository:

    @staticmethod
    def get_user(*, username: str, db: Session) -> Union[User, None]:
        """
        Getting user from db
        :param username: username
        :param db: session instance
        :return: user instance or none if no user exists.
        """
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def create_user(*, user: UserBase, db: Session) -> User:
        """
        Creating user in db
        :param user: user which must be created.
        :param db: session instance.
        :return: created user instance.
        """
        username, password = user.username, user.password
        user = User(
            username=username,
            hashed_password=Hash.get_password_hash(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)  # Update attributes from db
        return user

    @staticmethod
    def authenticate_user(user: User, password: str) -> Union[User, bool]:
        """
        Authenticating user by checking passsword
        :param user: user instance
        :param password: plain user password
        :return: user instance if passwords
        """
        if not Hash.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def update_activity(user: User, db: Session) -> User:
        """
        Updating user activity
        :param user: instance of user which should be updated
        :param db: session instance
        :return: updated user instance
        """
        user.last_logged = datetime.utcnow()
        db.commit()
        return user
