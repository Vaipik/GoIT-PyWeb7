from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api.dependecies import get_db
from api.config.config import app_config
from api.schemas.auth import TokenData
from api.models.users import User
from api.repositories.users import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Creating acces token by encoding data by using secret key and encoding algorithm.
    :param data: data which must be encoded
    :param expires_delta: lifetime of token.
    :return: encoded jwt token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(app_config["auth"]["algorithm"])
        )
    to_encode.update({"exp": expire})  # updating expire time for token
    encoded_jwt = jwt.encode(to_encode, app_config["auth"]["secret_key"], algorithm=app_config["auth"]["algorithm"])
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Authenticating user by jwt token.
    :param token: jwt token
    :param db: session instance
    :return: user if jwt is valid or raise 401 exception if credentials is not valid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #
        payload = jwt.decode(token, app_config["auth"]["secret_key"], algorithms=app_config["auth"]["algorithm"])
        username: str = payload.get("sub")  # extacting subject from encrypted data
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = UserRepository.get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user
