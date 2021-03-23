from core.database import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.types import ARRAY


class News(Base):
    """Модель новости"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)

    link = Column(String, unique=True, index=True)
    title = Column(String)
    image = Column(String)
    content = Column(ARRAY(Text))
