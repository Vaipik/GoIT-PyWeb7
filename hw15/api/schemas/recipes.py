from pydantic import BaseModel, Field


class Recipe:
    title: str
    # text: str = Field