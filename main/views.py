from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from garages.models import Garage


class MainPage(TemplateView):
    template_name = 'main/index.html'


class Dashboard(TemplateView, LoginRequiredMixin):

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
        return context