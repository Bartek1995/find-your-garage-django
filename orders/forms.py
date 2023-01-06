from django import forms

from cars.models import Car
from .models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Form for creating new order.
    """
    
    car = forms.ModelChoiceField(label="Wybór pojazdu", queryset=Car.objects.all())
    
    class Meta:
        model = Order
        fields = ['car', 'description']

    def __init__(self, user, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(user=user)
        
        
class ChangeOrderStateForm(forms.ModelForm):
    """
    Form for changing order state.
    """
    
    class Meta:
        model = Order
        fields = ['state']

    def __init__(self, *args, **kwargs):
        super(ChangeOrderStateForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['class'] = 'form-control'