from typing import List, Union

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    image: Union[str, None]
    content: List[str]

    class Config:
        orm_mode = True


class NewsList(NewsBase):
    id: int


class NewsCreate(NewsBase):
    link: str
