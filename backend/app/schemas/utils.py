from graphene import Field, List, Dynamic, ObjectType, Int, Argument, Enum, String
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
from graphene_sqlalchemy import SQLAlchemyObjectType as SQLAlchemyObjectTypeBase
from graphene_sqlalchemy.registry import get_global_registry
from sqlalchemy import inspect
from sqlalchemy.orm import interfaces

# def SQLAlchemyResolver(self, _, obj, resolve_info, *args, **kwargs):
#     print("Meow")
#     return getattr(obj, resolve_info.field_name)


def createSQLAlchemyFieldArguments(schema):
    return {
        "column": Argument(schema.enumUniqueColumns,
                    description="Column to select from",
                    required=True
        ),
        "value": Argument(String,
                    description="Value to search for",
                    required=True
        )
    }


def SQLAlchemyFieldResolver(schema):
    def resolver(self, info, **kwargs):
        query = schema.get_query(info)
        columns = schema.dictUniqueColumns

        query = query.filter(
            columns[kwargs.get("column")] == kwargs.get("value")
        )

        return query.one_or_none()
    return resolver


class OrderEnum(Enum):
    ASC = 0
    DESC = 1


def createSQLAlchemyListArguments(schema, pagination=False):
    return {
        "limit": Argument(Int,
                        description="Limit list to x items"
                    ),
        "filter": Argument(List(String),
                        description="Value to filter by"
                    ),
        "filter_by": Argument(List(schema.enumColumns),
                        description="Column to filter by"
                    ),
        "order": Argument(List(OrderEnum),
                        description="Order query by"
                    ),
         "order_by": Argument(List(schema.enumColumns),
                        description="Columns to order by"
                    )
    }


# For resolving manytoone/manytomany relationships.
# See "createSQLAlchemyListArguments" above for possible arguments
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
    
        return query.all()
    return resolver


# Metaclass for remapping the relationship object types.
# This will allow for subqueries...
class SQLAlchemyObjectTypeMeta(type):
    def __init__(cls, name, bases, nmspc):

        # TODO: Lazy fix to bypass...
        if name == "SQLAlchemyObjectType": return

        # Create enum type for model columns
        cls.enumColumns = Enum("{}_columns".format(cls.__name__),
                [(column[0], count)
                    for count, column in enumerate(inspect(cls._meta.model).columns.items())
                        if column not in cls._meta.fields.keys()
                ]
            )

        # TODO: Lazy...
        cls.enumUniqueColumns = Enum("{}_uniquecolumns".format(cls.__name__),
                [(column[0], count)
                        for count, column in enumerate(inspect(cls._meta.model).columns.items())
                            if column not in cls._meta.fields.keys() and (column[1].unique or column[1].primary_key)
                ]
            )
        
        # Create dict for model column objects -- for resolver
        cls.dictColumns = {
            count: column[1]
                for count, column in enumerate(inspect(cls._meta.model).columns.items())
                    if column not in cls._meta.fields.keys()
        }

        # TODO: Lazy...
        cls.dictUniqueColumns = {
            count: column[1]
                for count, column in enumerate(inspect(cls._meta.model).columns.items())
                    if column not in cls._meta.fields.keys() and (column[1].unique or column[1].primary_key)
        }

        # Recreate the dynamic type (for relationship) to used custom arguments/resolver
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