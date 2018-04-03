from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from backend.app.models.base import base


def connect():
    engine = create_engine('postgresql://localhost/blake-stage')
    sesssion = sessionmaker(bind=engine)
    db_session = scoped_session(sesssion)

    base.query = db_session.query_property()

    return db_session



