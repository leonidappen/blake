from collections import OrderedDict

from graphene import ObjectType, Field, List, String, Boolean
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs

from .input import InputBase, ValidationError


class InputErrors(Exception):
    def __init__(self, message, errors):
        super().__init__(self, message)
        self.errors = errors


class MutationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def InputQueryListResolver(schema):
    def resolver(_, info, **kwargs):
        return [
             obj for name, obj in schema.inputs.items()
                if issubclass(obj.__class__, InputBase)
        ]
    return resolver


def InputMutationResolver(schema):
    def resolver(_, info, **kwargs):
        data, errors = {}, {}

        for name, input in schema.inputs.items():
            value = kwargs.get(name, None)

            if value:
                try:
                    data[name] = input.validate(value)
                except ValidationError as e:
                    errors[name]= str(e)
            else:
                data[name] = input.default
            
            if errors:
                raise InputErrors("", errors)

            return schema.mutate(None, info, **data)
    return resolver


class InputQuery(ObjectType):
    type = String()
    name = String()
    description = String()
    required = Boolean()
    default = String()


class InputMutation(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        _meta = MutationOptions(cls)

        _meta.fields = OrderedDict()
        for base in reversed(cls.__mro__):
            _meta.fields.update(
                yank_fields_from_attrs(base.__dict__, _as=Field)
            )

        input_class = getattr(cls, "Inputs", None)
        cls.inputs = {
            name: obj for name, obj in input_class.__dict__.items()
                if issubclass(obj.__class__, InputBase)
        }

        _meta.arguments = {
            name: obj.get_scalar() for name, obj in cls.inputs.items()
        }

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def queryField(cls):
        return List(
            InputQuery,
            resolver=InputQueryListResolver(cls)
        )

    @classmethod
    def mutationField(cls):
        return Field(
            cls,
            args=cls._meta.arguments,
            resolver=InputMutationResolver(cls)
        )
