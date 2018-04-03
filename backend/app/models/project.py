from sqlalchemy import Column, Text, Integer

from .base import Base


class Project(Base):
    name = Column(Text, nullable=False)
    number = Column(Integer, nullable=False)
    language = Column(Text, nullable=False)
    coutry = Column(Text, nullable=False)