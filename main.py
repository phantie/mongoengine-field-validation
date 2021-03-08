from __future__ import annotations
from types import MethodType
from copy import copy

import mongoengine as me

ValidationError = me.ValidationError

__all__ = ('Validator',)

class ValidatorMeta(type):

    def __new__(cls, name, bases, attrs):
        def wrap(f, m):
            def check(self, value):
                if not f(value):
                    raise ValidationError(m)
            return check

        attrs['m'] = attrs.get('__annotations__', {}).get('m', '')
        attrs['check'] = wrap(attrs.get('condition', lambda self, value: ...), attrs['m'])
        return super().__new__(cls, name, bases, attrs)()

class Validator(metaclass=ValidatorMeta):

    def __and__(self, other: Validator) -> Validator:
        this_check = self.check
        def check(self, value):
            this_check(value)
            other.check(value)
        
        self = copy(self)
        return self.swap_check(check)

    def __or__(self, other: Validator) -> Validator:
        this_check = self.check
        def check(self, value):
            try:
                this_check(value)
            except ValidationError as e:
                m1 = e.args[0]
                try:
                    other.check(value)
                except ValidationError as e:
                    m2 = e.args[0]

                    message = ' or '.join((m1, m2))
                    raise ValidationError(message)
        
        self = copy(self)
        return self.swap_check(check)

    def __call__(self, value):
        return self.check(value)

    def swap_check(self, check):
        self.check = MethodType(check, self)
        return self

Validator = Validator.__class__