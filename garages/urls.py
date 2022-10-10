from django.urls import path
from .views import GarageCreateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('create/', GarageCreateView.as_view(), name='garage_create'),
]
