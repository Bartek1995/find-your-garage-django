from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator
from django.core import serializers

from garages.models import Garage
from cars.models import Car

from json import dumps


@method_decorator(gzip_page, name='dispatch')
class MainPage(TemplateView):
    """
    Main page view, which is displayed as the main page, when user visits the website.
    """
    
    template_name = 'main/index.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    Based on user type dashboard view, it returns different template.
    """
    
    def get(self, *args, **kwargs):
        if self.request.user.is_customer:
            self.template_name = 'main/dashboard_customer.html'

        elif self.request.user.is_entrepreneur:
            self.template_name = 'main/dashboard_entrepreneur.html'
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        
        if self.request.user.is_entrepreneur:
            try:
                context['user_garage'] = Garage.objects.get(user=self.request.user)
            except Garage.DoesNotExist:
                context['user_garage'] = None
                
        elif self.request.user.is_customer:
            mocked_data = []
            try:
                context['user_cars'] = Car.objects.filter(user=self.request.user)
                if not context['user_cars']:
                    raise Car.DoesNotExist
                for car in context['user_cars']:
                    # MOCKING CARS COSTS TO CONSTRUCT CHARTS - IT'S TEMPORARY SOLUTION
                    car.mock_information_about_orders()
                    car_as_dict = car.__dict__
                    del car_as_dict['_state']
                    mocked_data.append(car_as_dict)
                
                dataJSON = dumps(mocked_data)
                context['user_cars_json'] = dataJSON
                
            except Car.DoesNotExist:
                context['user_cars'] = None
                
        return context
