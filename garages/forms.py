from django import forms
from .models import Garage, ServiceList


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
       
       
class GarageEditForm(forms.ModelForm):
    is_active = forms.BooleanField(widget=forms.CheckboxInput, label='Warsztat aktywny', required=False)
    
    class Meta:
        model = Garage
        fields = ['name', 'description', 'website_url', 'location', 'is_active']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': '5'})
        }
        
        
class ServiceListEditForm(forms.ModelForm):
    
    class Meta:
        model = ServiceList
        fields = '__all__'
        exclude = ['garage']
