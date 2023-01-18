from fastapi import APIRouter

from ..schemas.auth import UserInDB


router = APIRouter(
    prefix="/token",
    tags=["auth"]
)


@router.post(
    path="/",
    response_model=UserInDB
)
def login():
    pass
