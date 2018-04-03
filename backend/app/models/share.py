from sqlalchemy import Column, Text

from .base import Base


class Share(Base):
    path = Column(Text, unique=True, nullable=False)
