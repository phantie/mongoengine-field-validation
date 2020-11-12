from mongoengine import ValidationError
from contextlib import suppress

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
        attrs['m'] = attrs.get('__annotations__', {}).get('m', '')
        attrs['condition'] = cls.Wrap(attrs.get('condition', None), attrs['m'])
        return super().__new__(cls, name, bases, attrs)

class Validator(metaclass=ValidatorMeta):
    def __new__(cls, value):
        return cls.condition(value)

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
        for v in self.validators:
            with suppress(AssertionError):
                v(value)
                return
        else:
            raise ValidationError(f'{" or ".join(v.m for v in self.validators)}')