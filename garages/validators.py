from django.core.exceptions import ValidationError
from string import printable


def validate_special_characters(word):
    for char in word:
        if not(char.isalpha()) and char != " ":
            raise ValidationError("Nazwa warsztatu zawiera nieprawidłowe znaki.")


def validate_poland_country(word):
    if 'Poland' in word:
        raise ValidationError(
            "Znacznik warsztatu powinien znajdować sie na terytorium Polski.")