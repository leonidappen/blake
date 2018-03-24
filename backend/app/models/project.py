from app.extensions import db
from .base import Base


class Project(Base):
    name = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    language = db.Column(db.Text, nullable=False)
    coutry = db.Column(db.Text, nullable=False)