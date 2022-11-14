from django import forms
from .models import Car


class CarEditForm(forms.ModelForm):
    date_of_expiry_of_insurance = forms.DateField(label="Data ważności ubezpieczenia OC", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    date_of_expiry_of_technical_inspection = forms.DateField(label="Data ważności przeglądu technicznego", widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = Car
        fields = ['brand', 'model', 'vin_number', 'production_year', 'engine_capacity', 'gearbox_type', 'engine_type',
                  'engine_code', 'engine_power', 'body_type', 'date_of_expiry_of_insurance', 'date_of_expiry_of_technical_inspection']
