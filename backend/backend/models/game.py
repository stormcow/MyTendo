from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Game(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    image = Column(String, nullable=True, default=None)
    owned = Column(Boolean, index=True, default=False)
