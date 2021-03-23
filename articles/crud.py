from sqlalchemy.orm import Session

from . import models, schemas


def get_allnews(db: Session, limit: int = None):
    """Возвращаем список новостей"""
    if limit is not None:
        return db.query(models.News).limit(limit).all()
    return db.query(models.News).all()


def create_news(db: Session, item: schemas.NewsCreate):
    """Создение новой новости"""
    db_news = models.News(**item.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
