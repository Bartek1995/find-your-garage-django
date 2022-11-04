from django.urls import path
from .views import CarCreateViewVinDecoding, CarCreateViewSelectMethod, CarCreateViewManual

urlpatterns = [
    path('create/select_method', CarCreateViewSelectMethod.as_view(), name='car_create_select_method'),
    path('create/vin_decoding', CarCreateViewVinDecoding.as_view(), name='car_create_vin_decoding'),
    path('create/manual', CarCreateViewManual.as_view(), name='car_create_manual'),
]
