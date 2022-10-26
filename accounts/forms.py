from django import forms
from allauth.account.forms import SetPasswordField, PasswordField, SignupForm
from django.contrib.auth.models import Group

from main.validators import validate_special_characters_and_numbers
from .models import CustomUser

isCustomer = 'is_customer'
isEntrepreneur = 'is_entrepreneur'

type_of_user_account = [
    (isCustomer, 'Klient'),
    (isEntrepreneur, 'Przedsiębiorca')
]


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Imię', validators=[validate_special_characters_and_numbers(message="Imię nie może zawierać znaków specjalnych oraz cyfr")])
    last_name = forms.CharField(max_length=30, label='Nazwisko', validators=[validate_special_characters_and_numbers(message="Nazwisko nie może zawierać znaków specjalnych oraz cyfr")])
    email = forms.EmailField(required=True)
    password1 = SetPasswordField()
    password2 = PasswordField()
    usertype = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'd-none'}), choices=type_of_user_account, label='', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        match self.cleaned_data['usertype']:
            case "is_customer":
                group = Group.objects.get(name='Customer')
                user.is_customer = True
            case "is_entrepreneur":
                group = Group.objects.get(name='Entrepreneur')
                user.is_entrepreneur = True

        user.groups.add(group)
        user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Imię', validators=[validate_special_characters_and_numbers(message="Imię nie może zawierać znaków specjalnych oraz cyfr")])
    last_name = forms.CharField(max_length=30, label='Nazwisko', validators=[validate_special_characters_and_numbers(message="Nazwisko nie może zawierać znaków specjalnych oraz cyfr")])
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name']
