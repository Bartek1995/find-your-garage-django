from django.db import models
from accounts.models import CustomUser

from pyvin import VIN

import orders
from .validators import validate_vin
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime
import json
import random

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

MANUAL = 'Manualna'
AUTOMATIC = 'Automatyczna'
SEMI_AUTOMATIC = 'Półautomatyczna'

GEARBOX_TYPE_CHOICES = (
    (MANUAL, 'Manualna'),
    (AUTOMATIC, 'Automatyczna'),
    (SEMI_AUTOMATIC, 'Półautomatyczna'),
)
    
    
HATCHBACK = 'Hatchback'
COMBI = 'Combi'
SEDAN = 'Sedan'
COUPE = 'Coupe'
CABRIOLLET = 'Kabriolet'
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
    
    brand = models.CharField(verbose_name="Marka", max_length=50, null=False, blank=False)
    model = models.CharField(verbose_name="Model", max_length=50, null=False, blank=False)
    vin_number = models.CharField(verbose_name="Numer VIN", validators=[validate_vin], max_length=17, null=False, blank=False)
    engine_capacity = models.PositiveIntegerField(verbose_name="Pojemność silnika", null=True, blank=True)
    production_year = models.IntegerField(verbose_name="Rok produkcji", validators=[MinValueValidator(1970, message="Rok produkcji nie może być mniejszy niż 1970"), MaxValueValidator(actual_year, message=f"Rok produkcji nie może być wyższy niż {actual_year}.")], null=True, blank=False)
    engine_type = models.CharField(verbose_name="Rodzaj silnika", choices=ENGINE_TYPE_CHOICES, max_length=50, null=True, blank=True)
    gearbox_type = models.CharField(verbose_name="Rodzaj skrzyni biegów", choices=GEARBOX_TYPE_CHOICES, max_length=50, null=True, blank=True)
    engine_power = models.PositiveIntegerField(verbose_name="Moc silnika", null=True, blank=True)
    engine_code = models.CharField(verbose_name="Kod silnika", max_length=30, null=True, blank=True)
    body_type = models.CharField(verbose_name="Typ nadwozia", choices=BODY_TYPE_CHOICES, max_length=50, null=True, blank=True)
    date_of_expiry_of_insurance = models.DateField(verbose_name="Data ważności ubezpieczenia OC", null=True, blank=False)
    date_of_expiry_of_technical_inspection = models.DateField(verbose_name="Data ważności przeglądu technicznego", null=True, blank=False)
    
    def __str__(self):
        return f"{self.vin_number} - {self.brand} {self.model} {self.production_year}"
    
    def mock_information_about_orders(self):
        """
        Temporary method to mock information about orders.
        """
        self.cost_of_repairs = random.randint(100, 5000)
        self.cost_of_parts = random.randint(100, 5000)
        self.cost_of_anothers = random.randint(100, 5000)
    
    @property
    def get_last_order(self):
        """
        Returns the last order for the car.
        """
        return orders.models.Order.objects.filter(car=self).order_by('created').first()
    
    @property
    def date_of_expiry_of_insurance_is_past_due(self):
        temp_date_of_expiry_of_insurance = datetime.datetime.strptime(self.date_of_expiry_of_insurance, "%Y-%m-%d")
        return date.today() < temp_date_of_expiry_of_insurance
    
    @property
    def date_of_expiry_of_technical_inspection_is_past_due(self):
        temp_date_of_expiry_of_technical_inspection = datetime.datetime.strptime(self.date_of_expiry_of_technical_inspection, "%Y-%m-%d")
        return date.today() < temp_date_of_expiry_of_technical_inspection