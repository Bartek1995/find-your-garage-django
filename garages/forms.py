from django import forms
from .models import Garage, ServiceList, OpeningHours


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


class GarageEditOpeningHoursForm(forms.ModelForm):
    from_hour = forms.TimeField(label="Godzina otwarcia", required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    to_hour = forms.TimeField(label="Godzina zamknięcia", required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = OpeningHours
        fields = ['from_hour', 'to_hour']
        
    def clean(self):
        if self.cleaned_data['from_hour'] is not None and self.cleaned_data['to_hour'] is None or self.cleaned_data['from_hour'] is None and self.cleaned_data['to_hour'] is not None:
            raise forms.ValidationError('Oba pola muszą być wypełnione.')
        
        if self.cleaned_data['from_hour'] and self.cleaned_data['to_hour']:
            if self.cleaned_data['from_hour'] > self.cleaned_data['to_hour']:
                raise forms.ValidationError('Godzina otwarcia nie może być późniejsza niż godzina zamknięcia.')
            return super().clean()