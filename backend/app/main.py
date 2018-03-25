from flask import Blueprint

from app.extensions import db
from app.schemas import schema
from app.schemas.utils import GraphQLView


blueprint = Blueprint("main", __name__)


blueprint.add_url_rule('/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        context={
            "session": db.session
        }
    )
)