from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from src.database.base import Base


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, unique=True)
    title: Mapped[str] = Column(String(50))
    text: Mapped[str] = Column(String(500))

    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)

