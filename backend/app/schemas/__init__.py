from graphene import Schema, ObjectType, Field, List, Int, String, Dynamic, Argument

from .utils import (SQLAlchemyObjectType,
                                        SQLAlchemyListResolver,
                                        createSQLAlchemyListArguments,
                                        SQLAlchemyFieldResolver,
                                        createSQLAlchemyFieldArguments
                                    )
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

    role = Field(RoleSchema,
        args=createSQLAlchemyFieldArguments(RoleSchema),
        resolver=SQLAlchemyFieldResolver(RoleSchema)
    )

    users = List(UserSchema,
        args=createSQLAlchemyListArguments(UserSchema),
        resolver=SQLAlchemyListResolver(UserSchema)
    )

    user = Field(UserSchema,
        args=createSQLAlchemyFieldArguments(UserSchema),
        resolver=SQLAlchemyFieldResolver(UserSchema)
    )


schema = Schema(query=Query)
