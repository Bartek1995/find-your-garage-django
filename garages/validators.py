from django.core.exceptions import ValidationError


def validate_poland_country(word):
    if 'Poland' not in word:
        raise ValidationError(
            "Znacznik warsztatu powinien znajdować sie na terytorium Polski.")
