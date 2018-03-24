from app.extensions import db
from .base import Base


class Share(Base):
    path = db.Column(db.Text, unique=True, nullable=False)
