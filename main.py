from __future__ import annotations
from types import MethodType
from copy import copy

from mongoengine import ValidationError


__all__ = ('Validator',)


class ValidatorMeta(type):

    def __new__(cls, name, bases, attrs):
        def wrap(f, m):
            def check(self, value):
                if not f(value):
                    raise ValidationError(m)
            return check

        attrs['check'] = wrap(attrs['condition'], attrs['__annotations__']['m'])
        return super().__new__(cls, name, bases, attrs)()

def prepare(Validator):
    Validator = Validator.__class__
    del Validator.__annotations__
    del Validator.condition
    return Validator

@prepare
class Validator(metaclass=ValidatorMeta):
    m: 'TEMP'
    condition = lambda self, value: False


    def __and__(self, other: Validator) -> Validator:
        this_check = self.check
        def check(self, value):
            this_check(value)
            other.check(value)
        
        return self.with_new_check(check)

    def __or__(self, other: Validator) -> Validator:
        this_check = self.check
        def check(self, value):
            try:
                this_check(value)
            except ValidationError as e1:
                try:
                    other.check(value)
                except ValidationError as e2:
                    raise ValidationError(' or '.join((e1.args[0], e2.args[0])))

        return self.with_new_check(check)

    def __call__(self, value):
        return self.check(value)

    def with_new_check(self, check):
        self = copy(self)
        self.check = MethodType(check, self)
        return self