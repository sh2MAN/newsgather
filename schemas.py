from pydantic import BaseModel
from typing import List, Optional, Type, Any


class News(BaseModel):
    title: str
    image: str
    content: List[str]


class Result(BaseModel):
    results: List[News]
