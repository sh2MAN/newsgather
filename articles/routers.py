from typing import List

from core import utils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import create_news, get_allnews
from .schemas import NewsCreate, NewsList

router = APIRouter()


@router.get('/news', response_model=List[NewsList])
def news_list(db: Session = Depends(utils.get_db)):
    return get_allnews(db)


@router.post('/news', response_model=NewsCreate)
def news_create(item: NewsCreate, db: Session = Depends(utils.get_db)):
    return create_news(db, item)
