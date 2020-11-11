from main import *
from mongoengine import Document, StringField

def TypeValidator(_type):
    class TypeValidator(Validator):
        m: f'Value must be of {_type!r} type'
        condition = lambda value: isinstance(value, _type)
    return TypeValidator

def LengthValidator(max_len, min_len = 0):
    assert min_len <= max_len
    class LengthValidator(Validator):
        m: f'Length must be in [{min_len}:{max_len}]'
        condition = lambda value: len(value) <= max_len and len(value) >= min_len
    return LengthValidator

class TitledValidator(Validator):
    m: 'Must be titled'
    condition = lambda value: value.istitle()

class CapitalizedValidator(Validator):
    m: 'Must be capitalized'
    condition = lambda value: all(l.isupper() for l in value)

class NoNumbersValidator(Validator):
    m: 'Don`t use numbers'
    condition = lambda value: not any(i.isdigit() for i in value)

class AlphaNumericValidator(Validator):
    m: 'Special symbols not allowed'
    condition = lambda value: value.isalnum()

StringTypeValidator = TypeValidator(str)


class Validation:
    nickname = CombinedValidator(
        StringTypeValidator,
        LengthValidator(21),
        AlphaNumericValidator,
    )

    name = CombinedValidator(
        StringTypeValidator,
        LengthValidator(24),
        NoNumbersValidator,
        TitledValidator,
        AlphaNumericValidator,
    )

    surname = name

    country = CombinedValidator(
        StringTypeValidator,
        LengthValidator(24),
        NoNumbersValidator,
        OR(
            TitledValidator,
            CapitalizedValidator,
        ),
        AlphaNumericValidator,
    )

    city = country


class User(Document):
    nickname = StringField(validation=Validation.nickname)
    name = StringField(validation=Validation.name)
    surname = StringField(required=False, validation=Validation.surname)
    country = StringField(required=False, validation=Validation.country)
    city = StringField(required=False, validation=Validation.city)

User(
    nickname='phantie',
    name='Alex',
    city='Odessa').validate()