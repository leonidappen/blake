import six
from flask_graphql import GraphQLView as GraphQLViewBase
from graphql.error import GraphQLError
from graphql.error import format_error as format_graphql_error

from ..inputs import MutationError
from ..inputs.mutation import InputErrors


# To catch custom exceptions and format them correctly in errors
def format_error(error):
    if hasattr(error, "original_error"):
        if isinstance(error.original_error, InputErrors):
            return {
                "inputs": error.original_error.errors
            }
        if isinstance(error.original_error, MutationError):
            return {
                "mutation": str(error.original_error)
            }

    if isinstance(error, GraphQLError):
        return format_graphql_error(error)

    return {'message': six.text_type(error)}


class GraphQLView(GraphQLViewBase):
    format_error = staticmethod(format_error)