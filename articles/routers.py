from typing import List

from core import utils
from fastapi import APIRouter, Depends, Query
from grabber import Grabber
from sqlalchemy.orm import Session

from .crud import create_news, get_all_news, get_news_by_link
from .schemas import NewsCreate, NewsList

router = APIRouter()


@router.get('/news', response_model=List[NewsList])
def news_list(
    db: Session = Depends(utils.get_db),
    limit: int = Query(None, gt=0, description='Количество новостей')
):
    grabber = Grabber()
    data = grabber.lenta.news(limit)

    for event in data:
        news = get_news_by_link(db, event.get('link'))
        if news is None:
            news = grabber.lenta.grub(event.get('link'))
            news = NewsCreate(**news, pub_date=event.get('published'))
            create_news(db, news)

    return get_all_news(db, limit)


@router.post('/news', response_model=NewsCreate)
def news_create(item: NewsCreate, db: Session = Depends(utils.get_db)):
    return create_news(db, item)
