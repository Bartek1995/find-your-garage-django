from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from .decorators import allowed_users
from .forms import GarageForm
from .models import Garage


@method_decorator(allowed_users(allowed_groups=['Entrepreneur']), name='dispatch')
class GarageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'garages/garage_create.html'
    form_class = GarageForm
    success_url = '/dashboard'

    def test_func(self):
        try:
            is_garage_exist = Garage.objects.get(user=self.request.user)
        except Garage.DoesNotExist:
            is_garage_exist = False
        return not(is_garage_exist)

    def handle_no_permission(self):
        self.request.messages = messages.warning(
            self.request, message='Istnieje już zarejestrowany warsztat na to konto użytkownika')
        return redirect('/dashboard')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(
            self.request, 'Warsztat został pomyślnie utworzony.')
        return super().form_valid(form)
