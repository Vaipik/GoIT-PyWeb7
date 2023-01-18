from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..dependecies import get_db
from ..schemas.users import UserBase, UserResponse, UserExists
from ..repositories.users import UserRepository


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="User created",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": UserExists}
    }
)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    _user = UserRepository.get_user(username=user.username, db=db)
    if _user is not None:
        return JSONResponse(
            content={
                "username": user.username,
                "message": "User with given username already exists"
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    _user = UserRepository.create_user(user=user, db=db)
    return _user

