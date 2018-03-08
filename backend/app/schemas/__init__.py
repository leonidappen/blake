from graphene import Schema, ObjectType, Field, List, Int, String, Dynamic, Argument

from .utils import SQLAlchemyObjectType, SQLAlchemyListResolver, createSQLAlchemyListArguments
from app.models import Role, User


class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User


class RoleSchema(SQLAlchemyObjectType):
    class Meta:
        model = Role


class Query(ObjectType):
    roles = List(RoleSchema,
        args=createSQLAlchemyListArguments(RoleSchema),
        resolver=SQLAlchemyListResolver(RoleSchema)
    )

    users = List(UserSchema,
        args=createSQLAlchemyListArguments(UserSchema),
        resolver=SQLAlchemyListResolver(UserSchema)
    )

    user = Field(UserSchema, id=Int(), name=String())

    # TODO: Resolving by fields
    def resolve_user(self, info, *args, **kwargs):
        query = UserSchema.get_query(info)
        return query.get(kwargs['id'])


schema = Schema(query=Query)
