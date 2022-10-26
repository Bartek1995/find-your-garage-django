from django.contrib import messages
from django.views.generic.edit import UpdateView
from .forms import ProfileEditForm
from .models import CustomUser


class ProfileEditView(UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'account/profile_edit.html'
    success_url = "/dashboard"

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        return super().get(self, request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Dane zostały zaktualizowane")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, "Popraw dane w formularzu aby zatwierdzić zmiany")
        return super().form_invalid(form)