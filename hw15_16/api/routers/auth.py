from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependecies import get_db
from api.libs.oath2 import create_access_token
from api.schemas.auth import Token, Unauthorized
from api.repositories.users import UserRepository


router = APIRouter(prefix="/token", tags=["auth"])


@router.post(
    path="/",
    response_model=Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": Unauthorized}},
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = UserRepository.get_user(username=form_data.username, db=db)
    if user is None or not UserRepository.authenticate_user(
        user=user, password=form_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserRepository.update_activity(user=user, db=db)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
