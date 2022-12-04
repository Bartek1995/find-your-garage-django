from django.db import models

from garages.models import Garage
from cars.models import Car
from accounts.models import CustomUser


ORDER_STATE = (
    (1, 'Oczekujące na akceptację'),
    (2, 'Zaakceptowane'),
    (3, 'W trakcie realizacji'),
    (4, 'Zrealizowane'),
    (5, 'Odrzucone'),
    (6, 'Wstrzymane'),
    (7, 'Oczekiwanie na akceptacje zmian'),
)


class Order(models.Model):
    
    garage = models.OneToOneField(Garage, on_delete=models.CASCADE, blank=False)
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    car = models.OneToOneField(Car, on_delete=models.SET_NULL, null=True, blank=False)
    
    state = models.PositiveSmallIntegerField(verbose_name="Status", choices=ORDER_STATE, default=1)
    created = models.DateTimeField(verbose_name="Data utworzenia", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="Data modyfikacji", auto_now=True)
    description = models.TextField(verbose_name="Opis", blank=True)


TYPE_OF_EXPENDITURE = (
    (1, 'Części'),
    (2, 'Usługa'),
    (3, 'Inne'),
)


class Expenditure(models.Model):
    
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, blank=False)
    
    type_of_expenditure = models.CharField(verbose_name="Typ wydatku", max_length=10, choices=TYPE_OF_EXPENDITURE, blank=False)
    name = models.CharField(verbose_name="Nazwa wydatku", max_length=50, blank=False)
    price = models.DecimalField(verbose_name="Cena", max_digits=10, decimal_places=2, blank=False)
    created = models.DateTimeField(verbose_name="Data utworzenia", auto_now_add=True)