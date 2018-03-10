from graphene import Schema, ObjectType

from .user import Query as UserQuery        
    

class Query(UserQuery, ObjectType):
    pass


schema = Schema(
    query=Query
)
