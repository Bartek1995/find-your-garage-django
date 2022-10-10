from django.urls import path
from .views import Dashboard, MainPage
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
]
