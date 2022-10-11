from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GarageForm


class GarageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'garages/garage_create.html'
    form_class = GarageForm
    success_url = '/dashboard'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        self.request.messages = messages.success(self.request, 'Warsztat został pomyślnie utworzony.')
        return super().form_valid(form)
