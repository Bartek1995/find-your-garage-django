from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Car
import requests

from accounts.mixins import GroupRequiredMixin


class CarCreateViewSelectMethod(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'cars/car_create_select_method.html'
    required_group = "Customer"


class CarCreateViewVinDecoding(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Car
    fields = ['vin_number', 'production_year']
    template_name = 'cars/car_create_vin_decoding.html'
    success_url = '/dashboard'
    required_group = "Customer"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.cleaned_data['vin_number'] = form.cleaned_data['vin_number'].upper()

        try:
            vin_checking_request = requests.get(
                f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{form.cleaned_data['vin_number']}*BA?format=json&modelyear={form.cleaned_data['production_year']}")
        except requests.exceptions.ConnectionError:
            self.request.messages = messages.error(
                self.request, "Nie udało się połączyć z serwerem dekodera VIN. Spróbuj ponownie później lub skorzystaj z formularza ręcznego.")
            return redirect('car_create_select_method')
        else:
            if vin_checking_request.status_code == 200:
                vin_checking_request_as_json = vin_checking_request.json()

                for record in vin_checking_request_as_json['Results']:
                    if record['Variable'] == 'Make' and record['Value'] is not None:
                        form.instance.brand = record['Value'].capitalize()

                    if record['Variable'] == 'Model' and record['Value'] is not None:
                        form.instance.model = record['Value'].capitalize()

                    if record['Variable'] == 'Displacement (CC)' and record['Value'] is not None:
                        converted_engine_capacity = int(float(record['Value']))
                        form.instance.engine_capacity = converted_engine_capacity

                    if record['Variable'] == 'Engine Model' and record['Value'] is not None:
                        form.instance.engine_code = record['Value'].upper()
            else:
                self.request.messages = messages.error(
                    self.request, "Wystąpił błąd podczas sprawdzania danych VIN. Spróbuj ponownie później lub skorzystaj z formularza ręcznego.")
                return redirect('car_create_select_method')

        self.request.messages = messages.success(
            self.request, 'Samochód został dodany do bazy danych.')
        return super().form_valid(form)


class CarCreateViewManual(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Car
    fields = ['brand', 'model', 'vin_number', 'production_year', 'engine_capacity',
              'gearbox_type', 'engine_type', 'engine_code', 'engine_power', 'body_type', ]
    template_name = 'cars/car_create_manual.html'
    success_url = '/dashboard'
    required_group = "Customer"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(
            self.request, 'Samochód został dodany do bazy danych.')
        return super().form_valid(form)
