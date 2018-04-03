from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr


base = declarative_base()


class Base(base):
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        return "{}s".format(cls.__name__.lower())

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, default=func.now(),
                            nullable=False)
    modified = Column(TIMESTAMP, default=func.now(),
                            onupdate=func.now(), nullable=False)
    active = Column(Boolean, default=True, nullable=False)