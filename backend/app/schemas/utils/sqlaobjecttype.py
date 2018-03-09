from graphene import (
    ObjectType,
    Argument,
    Dynamic,
    Field,
    List,
    Enum,
    String,
    Int
)
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
from graphene_sqlalchemy import SQLAlchemyObjectType as SQLAlchemyObjectTypeBase
from sqlalchemy import inspect
from sqlalchemy.orm import interfaces


# Arguments to query by unique value
# Values: are unique columns and primary keys (from model)
# TODO: Rewrite it so the key: value is column: value instead of passing two arguments
def createSQLAlchemyFieldArguments(schema):
    return {
        "column": Argument(
            schema.enumUniqueColumns,
            description="Column to select from",
            required=True
        ),
        "value": Argument(
            String,
            description="Value to search for",
            required=True
        )
    }


# Resolver to process arguments (See: createSQLAlchemyFieldArguments)
def SQLAlchemyFieldResolver(schema):
    def resolver(self, info, **kwargs):
        query = schema.get_query(info)
        columns = schema.dictUniqueColumns

        query = query.filter(
            columns[kwargs.get("column")] == kwargs.get("value")
        )

        return query.one_or_none()
    return resolver


# Helper method for definine query root Fields
def SQLAlchemyField(schema):
    return Field(
        schema,
        args=createSQLAlchemyFieldArguments(schema),
        resolver=SQLAlchemyFieldResolver(schema) 
    )


# SQLA Order Types
class OrderEnum(Enum):
    ASC = 0
    DESC = 1


# Arguments to query by SQLA functions
# Values: .limit(int) (limit), .filter(col=val) (filter), .order_by(col=asc/desc) (order)
def createSQLAlchemyListArguments(schema):
    return {
        "limit": Argument(
            Int,
            description="Limit list to x items"
        ),
        "filter": Argument(
            List(String),
            description="Value to filter by"
        ),
        "filter_by": Argument(
            List(schema.enumColumns),
            description="Column to filter by"
        ),
        "order": Argument(
            List(OrderEnum),
            description="Order query by"
        ),
         "order_by": Argument(
            List(schema.enumColumns),
            description="Columns to order by"
        ),
        "per_page": Argument(
            Int,
            description="Page size"
        ),
        "page": Argument(
            Int,
            description="Page number"
        )
    }


# Resolver to process arguments (See: createSQLAlchemyListArguments)
def SQLAlchemyListResolver(schema):
    def resolver(self, info, **kwargs):
        query = schema.get_query(info)
        columns = schema.dictColumns

        filter = kwargs.get("filter", None)
        filter_by = kwargs.get("filter_by", None)
        if filter and filter_by:
            for filter, filter_by in zip(filter, filter_by):
                query = query.filter(*{
                    columns[filter_by] == filter
                })

        order = kwargs.get("order", None)
        order_by = kwargs.get("order_by", None)
        if order and order_by:
            for order, order_by in zip(order, order_by):
                query = query.order_by(*[
                    getattr(columns[order_by], "asc" if order == OrderEnum.ASC else "desc")()
                ])

        limit = kwargs.get("limit", None)
        if limit:
            query = query.limit(limit)

        per_page = kwargs.get("per_page", None)
        page = kwargs.get("page", None)
        if per_page and page:
            query = query.limit(per_page).offset((page - 1) * per_page)
    
        return query.all()
    return resolver


# Helper method for definine query root Lists
def SQLAlchemyList(schema):
    return List(
        schema,
        args=createSQLAlchemyListArguments(schema),
        resolver=SQLAlchemyListResolver(schema) 
    )


# Metaclass to update the graphene-sqlalchemy object type
class SQLAlchemyObjectTypeMeta(type):
    def __init__(cls, name, bases, nmspc):
        # Hacky to pass meta on base class
        if name == "SQLAlchemyObjectType": return

        # Enum of Model columns names
        cls.enumColumns = Enum(
            "{}_columns".format(cls.__name__), [
                (column[0], count)
                    for count, column in enumerate(inspect(cls._meta.model).columns.items())
                        if column not in cls._meta.fields.keys()
            ]
        )

        # Enum of unqiue Model columns names
        # TODO: Probably can refactor this to make it a bit cleaner
        cls.enumUniqueColumns = Enum(
            "{}_uniquecolumns".format(cls.__name__), [
                (column[0], count)
                    for count, column in enumerate(inspect(cls._meta.model).columns.items())
                        if column not in cls._meta.fields.keys() and (column[1].unique or column[1].primary_key)
            ]
        )
        
        # Dict of Model column objs
        cls.dictColumns = {
            count: column[1]
                for count, column in enumerate(inspect(cls._meta.model).columns.items())
                    if column not in cls._meta.fields.keys()
        }

        # Dict of unique Model column objs
        # TODO: Probably can refactor this to make it a bit cleaner
        cls.dictUniqueColumns = {
            count: column[1]
                for count, column in enumerate(inspect(cls._meta.model).columns.items())
                    if column not in cls._meta.fields.keys() and (column[1].unique or column[1].primary_key)
        }

        # Recreate the dynamic type (for relationship) to used custom arguments/resolver defined above
        for field_name, obj in cls._meta.fields.items():
            if type(obj) is Dynamic:
                def dynamic_type():
                    relationship = inspect(cls._meta.model).relationships[field_name]
                    schema_type = cls._meta.registry.get_type_for_model(relationship.mapper.entity)
                    if not schema_type:
                       return None
                    if relationship.direction is interfaces.MANYTOONE or not relationship.uselist:
                         return Field(schema_type,
                            args=createSQLAlchemyFieldArguments(schema_type),
                            resolver=SQLAlchemyFieldResolver(schema_type)
                         )
                    else:
                        return List(schema_type,
                            args=createSQLAlchemyListArguments(schema_type),
                            resolver=SQLAlchemyListResolver(schema_type)
                            )
                
                cls._meta.fields[field_name] = Dynamic(dynamic_type)


class _CombinedMeta(SQLAlchemyObjectTypeMeta, SubclassWithMeta_Meta):
    pass


class SQLAlchemyObjectType(SQLAlchemyObjectTypeBase, metaclass=_CombinedMeta):
    class Meta:
        abstract = True