from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
import requests

from .models import Car
from accounts.mixins import GroupRequiredMixin
from .forms import CarEditForm


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
    """
    View used for creating car manually
    """
    model = Car
    fields = ['brand', 'model', 'vin_number', 'production_year', 'engine_capacity',
              'gearbox_type', 'engine_type', 'engine_code', 'engine_power', 'body_type', 'date_of_expiry_of_insurance', 'date_of_expiry_of_technical_inspection']
    template_name = 'cars/car_create_manual.html'
    success_url = '/dashboard'
    required_group = "Customer"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(
            self.request, 'Samochód został dodany do bazy danych.')
        return super().form_valid(form)


class CarEditView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """
    View used for editing car.
    """
    model = Car
    form_class = CarEditForm
    template_name = 'cars/car_edit.html'
    success_url = reverse_lazy('car_list')
    required_group = "Customer"
    
    def get(self, request, *args, **kwargs):
        try:
            car = self.get_object()
        except Car.DoesNotExist:
            self.messages = messages.error(
                self.request, "Nie znaleziono pojazdu o podanym ID.")
            return redirect('/dashboard')
        if self.request.user.id == car.user_id:
            return super().get(request, *args, **kwargs)
        else:
            self.messages = messages.error(
                self.request, "Nie masz uprawnień do edycji tego pojazdu.")
            return redirect('/dashboard')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(
            self.request, 'Samochód został zaktualizowany.')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return Car.objects.get(id=self.kwargs['car_id'])


class CarListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """
    View used for listing cars of logged user.
    """
    template_name = 'cars/car_list.html'
    required_group = "Customer"

    def get_queryset(self):
        return Car.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = self.get_queryset()
        return context


class CarDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    """
    View used for deleting car. User can delete only his own cars. It's impossible to delete car by entering car_id in URL. User must use delete button on car_list page and send POST request.
    """
    model = Car
    required_group = "Customer"
    success_url = '/dashboard'

    def get(self, request, *args, **kwargs):
        self.messages = messages.error(
            self.request, "Skorzystaj z przycisku usuń, korzystając z funkcji wyświetlenia listy pojazdów, aby usunąć pojazd.")
        return redirect('/dashboard')

    def post(self, *args, **kwargs):
        try:
            car = self.get_object()
        except Car.DoesNotExist:
            self.messages = messages.error(
                self.request, "Nie znaleziono pojazdu o podanym ID.")
            return redirect('/dashboard')

        if self.request.user.id == car.user_id:
            self.messages = messages.success(
                self.request, "Pojazd został usunięty")
            return super().post(*args, **kwargs)
        else:
            self.messages = messages.error(
                self.request, "Nie masz uprawnień do usunięcia tego pojazdu.")
            return redirect('/dashboard')

    def get_object(self, queryset=None):
        return Car.objects.get(id=self.kwargs['car_id'])
