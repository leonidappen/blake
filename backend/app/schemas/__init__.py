from graphene import Schema, ObjectType

from app.models import Role, User
from .utils import (
    SQLAlchemyObjectType,
    SQLAlchemyList,
    SQLAlchemyField
)

class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User


class RoleSchema(SQLAlchemyObjectType):
    class Meta:
        model = Role


class Query(ObjectType):
    roles = SQLAlchemyList(RoleSchema)
    role = SQLAlchemyField(RoleSchema)
    
    users = SQLAlchemyList(UserSchema)
    user = SQLAlchemyField(UserSchema)


schema = Schema(query=Query)
