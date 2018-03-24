from sqlalchemy.ext.declarative import declared_attr

from app.extensions import db


class Base(db.Model):
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        return "{}s".format(cls.__name__.lower())

    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.TIMESTAMP, default=db.func.now(),
                            nullable=False)
    modified = db.Column(db.TIMESTAMP, default=db.func.now(),
                            onupdate=db.func.now(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)