from django.urls import path
from .views import GarageCreateView, GarageEditView, GarageDeleteView, GarageInformationView, ServiceListUpdateView


urlpatterns = [
    path('create/', GarageCreateView.as_view(), name='garage_create'),
    path('edit/<int:garage_id>', GarageEditView.as_view(), name='garage_edit'),
    path('edit/services/<int:garage_id>', ServiceListUpdateView.as_view(), name='garage_services_edit'),
    path('delete/<int:garage_id>', GarageDeleteView.as_view(), name='garage_delete'),
    path('information/<int:pk>', GarageInformationView.as_view(), name='garage_information'),
]
