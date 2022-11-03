from django.db import models
from accounts.models import CustomUser
from pyvin import VIN
from .validators import validate_vin
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# GET THE CURRENT YEAR
date = datetime.datetime.today()
actual_year = date.year


# DECLARATION OF ENGINE TYPES
PETROL = 'PB'
PETROL_LPG = 'PB+LPG'
DIESEL = 'ON'
HYBRID = 'HYB'
ELECTRIC = 'ELE'
OTHER = 'OTHER'

ENGINE_TYPE_CHOICES = (
    (PETROL, 'Benzyna'),
    (PETROL_LPG, 'Benzyna + LPG'),
    (DIESEL, 'Diesel'),
    (HYBRID, 'Hybryda'),
    (ELECTRIC, 'Elektryczny'),
    (OTHER, 'Inny'),
)

# DECLARATION OF GEARBOX TYPES

MANUAL = 'manual'
AUTOMATIC = 'automatic'
SEMI_AUTOMATIC = 'semi-automatic'

GEARBOX_TYPE_CHOICES = (
    (MANUAL, 'Manualna'),
    (AUTOMATIC, 'Automatyczna'),
    (SEMI_AUTOMATIC, 'Półautomatyczna'),
)
    
    
HATCHBACK = 'Hatchback'
COMBI = 'Combi'
SEDAN = 'Sedan'
COUPE = 'Coupe'
CABRIOLLET = 'Cabriollet'
SUV = 'SUV'
VAN = 'Van'
PICKUP = 'Pickup'

BODY_TYPE_CHOICES = (
    (HATCHBACK, 'Hatchback'),
    (COMBI, 'Combi'),
    (SEDAN, 'Sedan'),
    (COUPE, 'Coupe'),
    (CABRIOLLET, 'Kabriolet'),
    (SUV, 'SUV'),
    (VAN, 'Van'),
    (PICKUP, 'Pickup'),
)


class Car(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    brand = models.CharField(verbose_name="Marka", max_length=50, null=False, blank=True)
    model = models.CharField(verbose_name="Model", max_length=50, null=False, blank=True)
    vin_number = models.CharField(verbose_name="Numer VIN", validators=[validate_vin], max_length=17, null=False, blank=True)
    engine_capacity = models.IntegerField(verbose_name="Pojemność silnika", null=True, blank=True)
    production_year = models.IntegerField(verbose_name="Rok produkcji", validators=[MinValueValidator(1970, message="Rok produkcji nie może być mniejszy niż 1970"), MaxValueValidator(actual_year, message=f"Rok produkcji nie może być wyższy niż {actual_year}.")], null=True, blank=True)
    engine_type = models.CharField(verbose_name="Rodzaj silnika", choices=ENGINE_TYPE_CHOICES, max_length=50, null=True, blank=True)
    gearbox_type = models.CharField(verbose_name="Rodzaj skrzyni biegów", choices=GEARBOX_TYPE_CHOICES, max_length=50, null=True, blank=True)
    engine_power = models.IntegerField(verbose_name="Moc silnika", null=True, blank=True)
    engine_code = models.CharField(verbose_name="Kod silnika", max_length=30, null=True, blank=True)
    body_type = models.CharField(verbose_name="Typ nadwozia", choices=BODY_TYPE_CHOICES, max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vin_number} - {self.brand} {self.model} {self.production_year}"