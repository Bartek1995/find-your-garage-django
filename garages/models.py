import os
from django.db import models
from accounts.models import CustomUser
from places.fields import PlacesField
import googlemaps


class Garage(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    name = models.CharField(verbose_name="Name", max_length=100, null=True, blank=True)
    full_address = models.CharField(verbose_name="Full Address", max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name="City/Town", max_length=100, null=True, blank=True)
    street_number = models.CharField(verbose_name="Street Number", max_length=100, null=True, blank=True)
    street = models.CharField(verbose_name="Street", max_length=100, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=100, null=True, blank=True)
    postal_code = models.CharField(verbose_name="Postal Code", max_length=6, null=True, blank=True)
    place_id = models.CharField(verbose_name="Place ID", max_length=100, null=True, blank=True, unique=True)
    location = PlacesField()
    
    is_active = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs) -> None:
        """
        Override save method and initialize google maps api. Then geocode location field data, and save details in model fields.
        """
        gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
        reverse_geocode_result = gmaps.reverse_geocode((self.location.latitude, self.location.longitude))

        for component in reverse_geocode_result[0]['address_components']:
            match component['types'][0]:
                case 'route':
                    self.street = component['long_name']
                case 'street_number':
                    self.street_number = component['long_name']
                case 'locality':
                    self.city = component['long_name']
                case 'postal_code':
                    self.postal_code = component['long_name']
                case 'country':
                    self.country = component['long_name']

        self.full_address = reverse_geocode_result[0]['formatted_address']
        self.place_id = reverse_geocode_result[0]['place_id']
        self.is_active = True
        return super().save()
    
    def __str__(self) -> str:
        return f"{self.name} - {self.user.email}"