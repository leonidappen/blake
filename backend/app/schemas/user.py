from graphene import ObjectType

from .utils import (
    SQLAlchemyObjectType,
    SQLAlchemyList,
    SQLAlchemyField
)
from app.models import Role as RoleModel
from app.models import User as UserModel


class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password_hash",)


class Query(ObjectType):
    class Meta:
        abstract = True

    roles = SQLAlchemyList(Role)
    role = SQLAlchemyField(Role)

    users = SQLAlchemyList(User)
    user = SQLAlchemyField(User)
