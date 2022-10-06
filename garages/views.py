from django.views.generic.edit import CreateView
from .forms import GarageForm


class GarageCreateView(CreateView):
    template_name = 'garages/garage_create.html'
    form_class = GarageForm
    success_url = '/garage/create_complete'
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)
