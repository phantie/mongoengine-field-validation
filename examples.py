from main import *
from mongoengine import Document, StringField

def TypeValidator(_type):
    class TypeValidator(Validator):
        m: f'Value must be of "{_type.__name__}" type'
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

class OnlyNumbers(Validator):
    m: 'Use only numbers'
    condition = lambda value: all(i.isdigit() for i in value)

class OnlyAa(Validator):
    m: 'Use only `A` and `a` symbols'
    condition = lambda value: all(i.lower() == 'a' for i in value)


StringTypeValidator = TypeValidator(str)

class Validation:
    nickname = AND(
        StringTypeValidator,
        LengthValidator(21),
        AlphaNumericValidator,
    )

    name = AND(
        StringTypeValidator,
        LengthValidator(24),
        NoNumbersValidator,
        TitledValidator,
        AlphaNumericValidator,
    )

    surname = name

    country = AND(
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

#     city = (
#         StringTypeValidator &
#         LengthValidator(24) &
#         NoNumbersValidator &
#             (TitledValidator | CapitalizedValidator) &
#         AlphaNumericValidator
# )

    strange_creature = \
        AND(
            StringTypeValidator,
            OR (
                AND (
                    OnlyNumbers,
                    LengthValidator(min_len=2, max_len=4),
                ), 
                AND (
                    OnlyAa,
                    LengthValidator(10),
                ), 
            
            )
        )


class User(Document):
    nickname = StringField(validation=Validation.nickname)
    name = StringField(validation=Validation.name)
    surname = StringField(required=False, validation=Validation.surname)
    country = StringField(required=False, validation=Validation.country)
    city = StringField(required=False, validation=Validation.city)
    
    advanced_example = StringField(validation=Validation.strange_creature)


User(
    nickname='phantie',
    name='Alex',
    city='Odessa',
    
    advanced_example = '121231233').validate()