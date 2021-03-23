from core.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.types import ARRAY


class News(Base):
    """Модель новости"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    link = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    image = Column(String)
    content = Column(ARRAY(Text))
    pub_date = Column(DateTime)
