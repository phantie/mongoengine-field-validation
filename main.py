from mongoengine import ValidationError

__all__ = ('Validator', 'AND', 'OR')

class ValidatorMeta(type):
    class Wrap:
        def __init__(self, f, m):
            self.f = f
            self.m = m

        def __call__(self, *args, **kwargs):
            if not self.f(*args, **kwargs):
                raise ValidationError(self.m)

    def __new__(cls, name, bases, attrs):
        attrs['m'] = attrs['__annotations__']['m']
        attrs['condition'] = cls.Wrap(attrs['condition'], attrs['m'])
        return super().__new__(cls, name, bases, attrs)

class Validator(metaclass=ValidatorMeta):
    m: ''

    def __new__(cls, value):
        return cls.condition(value)

    def condition(value):
        raise Exception('Redefine this method in subclasses')

class ValidatorStore:
    def __init__(self, *validators):
        self.validators = validators
        self.m = ' and '.join(v.m for v in validators)

class AND(ValidatorStore):
    def __call__(self, value):
        for v in self.validators:
            v(value)

class OR(ValidatorStore):
    def __call__(self, value):
        return self.condition(value)

    def condition(self, value):
        for v in self.validators:
            try:
                v(value)
            except AssertionError:
                pass
            else:
                return
        else:
            raise ValidationError(f'{" or ".join(v.m for v in self.validators)}')