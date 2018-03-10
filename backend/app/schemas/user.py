from graphene import ObjectType

from .utils import (
    SQLAlchemyObjectType,
    SQLAlchemyList,
    SQLAlchemyField
)
from app.models import Role as RoleModel
from app.models import User as UserModel


class RoleSchema(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password_hash",)


class Query(ObjectType):
    class Meta:
        abstract = True

    roles = SQLAlchemyList(RoleSchema)
    role = SQLAlchemyField(RoleSchema)

    users = SQLAlchemyList(UserSchema)
    user = SQLAlchemyField(UserSchema)
