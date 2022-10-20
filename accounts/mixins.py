from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class GroupRequiredMixin(AccessMixin):

    required_group = None

    def dispatch(self, request, *args, **kwargs):
        if self.required_group is None:
            raise ImproperlyConfigured(
                "'GroupRequiredMixin' requires 'required_group' attribute to be set.")
        else:
            if self.request.user.groups.exists():
                group = request.user.groups.all()

            for key in group:
                if key.name == self.required_group:
                    return super().dispatch(request, *args, **kwargs)
                return self.handle_no_permission()
            else:
                return self.handle_no_permission()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request, 'Brak uprawnień do przeglądania tej strony')
            return redirect('dashboard')
        return super().handle_no_permission()