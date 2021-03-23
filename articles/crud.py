from sqlalchemy.orm import Session

from . import models, schemas


def get_all_news(db: Session, limit: int = None):
    """Возвращаем список новостей"""
    news = db.query(models.News).order_by(models.News.pub_date.desc()).all()
    if limit is not None:
        return news[:limit]
    return news


def get_news_by_link(db: Session, link: str):
    """Получаем новость по ссылке"""
    return db.query(models.News).filter(models.News.link == link).first()


def create_news(db: Session, item: schemas.NewsCreate):
    """Создение новой новости"""
    db_news = models.News(**item.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
