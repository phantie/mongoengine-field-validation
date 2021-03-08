from mongoengine import ValidationError

__all__ = ('Validator', 'AND', 'OR')

class ValidatorMeta(type):

    def __new__(cls, name, bases, attrs):
        def wrap(f, m):
            def wrap(*args, **kwargs):
                if not f(*args, **kwargs):
                    raise ValidationError(m)
            return wrap

        attrs['m'] = attrs.get('__annotations__', {}).get('m', '')
        attrs['condition'] = wrap(attrs.get('condition', None), attrs['m'])
        return super().__new__(cls, name, bases, attrs)

class Validator(metaclass=ValidatorMeta):
    def __new__(cls, value):
        return cls.condition(value)


class ValidatorStore:
    def __init__(self, *validators):
        self.validators = validators

class AND(ValidatorStore):
    def __call__(self, value):
        for v in self.validators:
            v(value)

    @property
    def m(self):
        return ' and '.join(v.m for v in self.validators)

class OR(ValidatorStore):
    def __call__(self, value):
        for v in self.validators:
            try: v(value)
            except AssertionError: ...
            else: return
        else:
            raise ValidationError(f'{" or ".join(v.m for v in self.validators)}')