from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..libs import constants


class UserBase(BaseModel):
    username: str = Field(
        min_length=constants.USERNAME_MIN_LENGTH,
        max_length=constants.USERNAME_MAX_LENGTH,
        example="username"  # does not work in extra_schema
    )
    password: str = Field(
        min_length=constants.PASSWORD_MIN_LENGTH,
        max_length=constants.PASSWORD_MAX_LENGTH,
        example="password"  # does not work in extra_schema
    )


class UserResponse(BaseModel):
    uuid: UUID
    username: str = Field(example="username")  # does not work in extra_schema
    is_active: bool = True
    last_logged: Optional[datetime]

    class Config:
        extra_schema = {
            "example": {
                "uuid": "960ef55d-1e2d-4a34-9dcb-d91d0ea468c7",
                "is_active": True,
                "last_logged": datetime.utcnow(),
            }
        }
        orm_mode = True


class UserExists(BaseModel):
    username: str
    message: str = Field(example="User with given name already exists")
