from django.core.exceptions import ValidationError
from vininfo import Vin


def validate_vin(vin):
    vin = vin.upper()
    if len(vin) == 17:
        for char in vin:
            if char.isalpha() or char.isnumeric():
                if char not in 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789':
                    raise ValidationError(
                        "Numer VIN zawiera niedozwolone znaki.")
            else:
                raise ValidationError(
                    "Numer VIN powinien zawierać tylko litery i cyfry.")
        car_vin = Vin(vin)
        if car_vin.manufacturer == 'UnsupportedBrand':
            raise ValidationError(
                "Nieprawidłowy numer VIN.")
    else:
        raise ValidationError("Numer VIN powinien zawierać 17 znaków.")
