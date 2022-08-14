from django import forms
from allauth.account.forms import SetPasswordField, PasswordField, SignupForm
from django.contrib.auth.models import Group

isCustomer = 'is_customer'
isEntrepreneur = 'is_entrepreneur'

type_of_user_account = [
    (isCustomer, 'Klient'),
    (isEntrepreneur, 'Przedsiębiorca')
]


class CustomSignupForm(SignupForm):
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
