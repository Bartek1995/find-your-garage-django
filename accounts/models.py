from django.db import models
from django.contrib.auth.models import AbstractUser

from address.models import AddressField

from myproject.azure_blob_storage import OverwriteStorage


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_entrepreneur = models.BooleanField(default=False)
    address = AddressField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, storage=OverwriteStorage())
