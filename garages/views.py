from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from accounts.mixins import GroupRequiredMixin

from .forms import GarageForm, GarageEditForm
from .models import Garage


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