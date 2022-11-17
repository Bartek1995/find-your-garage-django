from django.urls import path
from .views import GarageCreateView, GarageEditView, GarageDeleteView


urlpatterns = [
    path('create/', GarageCreateView.as_view(), name='garage_create'),
    path('edit/<int:garage_id>', GarageEditView.as_view(), name='garage_edit'),
    path('delete/<int:garage_id>', GarageDeleteView.as_view(), name='garage_delete'),
]
