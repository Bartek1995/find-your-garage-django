from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from accounts.mixins import GroupRequiredMixin
from .forms import GarageForm, GarageEditForm
from .models import Garage

import os


class GarageCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    """
    View for creating new garage.
    """
    template_name = 'garages/garage_create.html'
    form_class = GarageForm
    success_url = '/dashboard'
    required_group = "Entrepreneur"
    
    def get(self, *args, **kwargs):
        try:
            garage = Garage.objects.get(user=self.request.user)
        except Garage.DoesNotExist:
            pass
        else:
            self.request.messages = messages.warning(self.request, message='Istnieje już zarejestrowany warsztat na to konto użytkownika')
            return redirect('/dashboard')
        return super().get(self, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(
            self.request, 'Warsztat został pomyślnie utworzony.')
        return super().form_valid(form)


class GarageEditView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """
    View for editing garage.
    """
    template_name = 'garages/garage_edit.html'
    form_class = GarageEditForm
    success_url = '/dashboard'
    required_group = "Entrepreneur"
    
    def get(self, request, *args, **kwargs):
        try:
            garage = self.get_object()
        except Garage.DoesNotExist:
            self.messages = messages.error(
                self.request, "Nie znaleziono warsztatu o podanym ID.")
            return redirect('/dashboard')
        if self.request.user.id == garage.user_id:
            return super().get(request, *args, **kwargs)
        else:
            self.messages = messages.error(
                self.request, "Nie masz uprawnień do edycji tego warsztatu.")
            return redirect('/dashboard')
        
    def get_object(self, queryset=None):
        return Garage.objects.get(id=self.kwargs['garage_id'])

    def form_valid(self, form):
        self.request.messages = messages.success(
            self.request, 'Warsztat został zaktualizowany.')
        return super().form_valid(form)


class GarageDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    """
    View for deleting garage.
    """
    success_url = '/dashboard'
    required_group = "Entrepreneur"

    def get(self, request, *args, **kwargs):
        self.messages = messages.error(
            self.request, "Skorzystaj z przycisku usuń, w menu edycji warsztatu aby go skasować.")
        return redirect('/dashboard')

    def post(self, *args, **kwargs):
        try:
            garage = self.get_object()
        except Garage.DoesNotExist:
            self.messages = messages.error(
                self.request, "Nie znaleziono warsztatu o podanym ID.")
            return redirect('/dashboard')

        if self.request.user.id == garage.user_id:
            self.messages = messages.success(self.request, "Warsztat został pomyślnie usunięty.")
            return super().post(*args, **kwargs)
        else:
            self.messages = messages.error(
                self.request, "Nie masz uprawnień do usunięcia tego warsztatu.")
            return redirect('/dashboard')

    def get_object(self, queryset=None):
        return Garage.objects.get(id=self.kwargs['garage_id'])


class GarageInformationView(LoginRequiredMixin, DetailView):
    template_name = 'garages/garage_information.html'
    
    def get_queryset(self):
        return Garage.objects.filter(id=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_api_key'] = os.environ.get('GOOGLE_API_KEY')
        return context