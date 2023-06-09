from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.database.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = Column(Integer, primary_key=True, index=True, unique=True)
    username: Mapped[str] = Column(String, unique=True, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)

    def __str__(self):
        return f'{self.username}'
