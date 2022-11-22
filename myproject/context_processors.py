from garages.models import Garage


def user_garage(request):
    if request.user.groups.exists():
        group = request.user.groups.all()
        for key in group:
            if key.name == 'Entrepreneur':
                try:
                    garage = Garage.objects.get(user=request.user)
                except Garage.DoesNotExist:
                    return {}
                else:
                    return {'user_garage': garage}
            else:
                return {}
    else:
        return {}