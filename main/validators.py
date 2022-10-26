from django.core.exceptions import ValidationError
from functools import wraps


def validate_special_characters_and_numbers(message):
    @wraps(validate_special_characters_and_numbers)
    def inner_func(word):
        for char in word:
            if not(char.isalpha()) and char != " ":
                raise ValidationError(message)
    return inner_func
