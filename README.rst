.. code:: python

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

        city = (
            StringTypeValidator &
            LengthValidator(24) &
            NoNumbersValidator &
            (TitledValidator | CapitalizedValidator) &
            AlphaNumericValidator
        )

    class User(Document):
        nickname = StringField(validation=Validation.nickname)
        name = StringField(validation=Validation.name)
        city = StringField(required=False, validation=Validation.city)

    User(
        nickname='phantie',
        name='Alex',
        city='Odessa'
            ).validate()
