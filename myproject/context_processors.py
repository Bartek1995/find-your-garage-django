from garages.models import Garage


def user_garage(request):
    user_group = request.user.groups.all()[0].name
    if user_group == 'Entrepreneur':
        if request.user.is_authenticated:
            try:
                garage = Garage.objects.get(user=request.user)
            except Garage.DoesNotExist:
                return {'user_garage': None}
            else:
                return {'user_garage': garage}
        else:
            return {'user_garage': None}