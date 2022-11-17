from django.urls import path
from .views import GarageCreateView, GarageEditView


urlpatterns = [
    path('create/', GarageCreateView.as_view(), name='garage_create'),
    path('edit/<int:garage_id>', GarageEditView.as_view(), name='garage_edit'),
]
