import graphene


class ValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class InputBase(object):
    scalar = None

    def __init__(self, name, description, required=True, default=None):
        self.type = self.__class__.__name__
        self.name = name
        self.description = description
        self.required = required
        self.default = default
    
    def get_scalar(self):
        return self.scalar(
            name=self.name,
            description=self.description,
            required=self.required,
            default_value=self.default
        )

    def validate(self, value):
        return value
    

class String(InputBase):
    scalar = graphene.String


class Int(InputBase):
    scalar = graphene.Int


class Float(InputBase):
    scalar = graphene.Float


class Boolean(InputBase):
    scalar = graphene.Boolean
