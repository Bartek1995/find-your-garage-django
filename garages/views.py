from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from accounts.mixins import GroupRequiredMixin

from .forms import GarageForm
from .models import Garage


class GarageCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
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
