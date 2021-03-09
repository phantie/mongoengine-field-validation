from main import Validator

from contests import some, every
# pip install git+https://github.com/phantie/contests.git

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
    condition = lambda value: every(value).isupper()

class NoNumbersValidator(Validator):
    m: 'Don`t use numbers'
    condition = lambda value: not some(value).isdigit()

class AlphaNumericValidator(Validator):
    m: 'Special symbols not allowed'
    condition = lambda value: value.isalnum()

class OnlyNumbers(Validator):
    m: 'Use only numbers'
    condition = lambda value: every(value).isdigit()

class OnlyAa(Validator):
    m: 'Use only `A` and `a` symbols'
    condition = lambda value: every(value.lower()) == 'a'


StringTypeValidator = TypeValidator(str)




class Validation:
    nickname = (
        StringTypeValidator &
        LengthValidator(21) &
        AlphaNumericValidator
    )

    name = (
        StringTypeValidator &
        LengthValidator(24) &
        NoNumbersValidator &
        TitledValidator &
        AlphaNumericValidator
    )

    surname = name

    country = (
        StringTypeValidator &
        LengthValidator(24) &
        NoNumbersValidator &
        (TitledValidator | CapitalizedValidator) &
        AlphaNumericValidator
    )

    city = country

    strange_creature = (
            StringTypeValidator &
            (
                (OnlyNumbers & LengthValidator(min_len=2, max_len=4)) |
                (OnlyAa & LengthValidator(10))))


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

    advanced_example = '123').validate()