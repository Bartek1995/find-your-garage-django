from django.db import models
from django import forms
from .models import Garage


class GarageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GarageForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['nip_number'].required = True
    
    class Meta:
        model = Garage
        fields = ['name', 'nip_number',
                  'website_url', 'description', 'location']

        labels = {
            'name': 'Nazwa Twojego warsztatu',
            'nip_number': 'NIP',
            'website_url': 'Adres strony internetowej',
            'description': 'Dodatkowy opis warsztatu',
            'location': 'Adres',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': '5'})
        }
       
