from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPage(TemplateView):
    template_name = 'main/index.html'


class Dashboard(TemplateView, LoginRequiredMixin):
    template_name = 'main/dashboard.html'
