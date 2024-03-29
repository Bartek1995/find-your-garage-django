import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ServiceList, OpeningHours, Garage


@receiver(post_save, sender=Garage)
def create_additional_objects_with_garage_creating(sender, instance, created, **kwargs):
    """
    Function for creating additional objects with creating garage.
    If user create new garage, this function create new ServiceList and OpeningHours objects.
    """
    if created:
        ServiceList.objects.create(garage=instance)
        for i in range(1, 8):
            if i < 6:
                OpeningHours.objects.create(garage=instance, weekday=i, from_hour=datetime.time(8, 0), to_hour=datetime.time(16, 0))
            else:
                OpeningHours.objects.create(garage=instance, weekday=i)