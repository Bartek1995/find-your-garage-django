import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from main.validators import validate_special_characters_and_numbers
from .validators import validate_poland_country
from accounts.models import CustomUser
from places.fields import PlacesField
import googlemaps


class Garage(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    name = models.CharField(verbose_name="Nazwa", max_length=50, null=False, blank=True, validators=[validate_special_characters_and_numbers(message="Nazwa warsztatu nie może zawierać znaków specjalnych oraz cyfr")])
    nip_number = models.BigIntegerField(verbose_name="Numer NIP", null=False, blank=True, validators=[MaxValueValidator(9999999999, message="Niepoprawny numer NIP"), MinValueValidator(1000000000, message="Niepoprawny numer NIP")])
    description = models.TextField(verbose_name="Opis", max_length=300, null=True, blank=True)
    website_url = models.URLField(verbose_name="Adres URL", max_length=50, null=False, blank=True)
    full_address = models.CharField(verbose_name="Pełny adres", max_length=100, null=True, blank=True, validators=[validate_poland_country])
    city = models.CharField(verbose_name="Miejscowość", max_length=50, null=True, blank=True,)
    street_number = models.CharField(verbose_name="Numer budynku", max_length=10, null=True, blank=True)
    street = models.CharField(verbose_name="Ulica", max_length=100, null=True, blank=True)
    country = models.CharField(verbose_name="Kraj", max_length=30, null=True, blank=True)
    postal_code = models.CharField(verbose_name="Kod pocztoqy", max_length=20, null=True, blank=True)
    place_id = models.CharField(verbose_name="ID miejsca", max_length=100, null=True, blank=True, unique=True)
    location = PlacesField()
    
    is_active = models.BooleanField(default=False)
    
    def clean(self) -> None:
        """
        Override clean method and initialize google maps api. Then geocode location field data, and save details in model fields.
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
        
        return super().clean()
    
    def __str__(self) -> str:
        return f"{self.name} - {self.user.email}"