from pydantic import BaseModel, Field


class Recipe(BaseModel):
    title: str
    text: str

    class Config:
        example = {
            "title"
        }