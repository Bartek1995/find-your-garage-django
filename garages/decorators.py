from django.shortcuts import redirect
from django.contrib import messages


def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.exists():
                group = request.user.groups.all()

            for key in group:
                if key.name in allowed_groups:
                    return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 'Brak uprawnień do przeglądania tej strony')
                return redirect('dashboard')
        return wrapper_func
    return decorator
