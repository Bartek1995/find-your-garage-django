from django.urls import path
from .views import CarCreateViewVinDecoding, CarCreateViewSelectMethod, CarCreateViewManual, CarEditView, CarListView, CarDeleteView

urlpatterns = [
    path('create/select_method', CarCreateViewSelectMethod.as_view(),
         name='car_create_select_method'),
    path('create/vin_decoding', CarCreateViewVinDecoding.as_view(),
         name='car_create_vin_decoding'),
    path('create/manual', CarCreateViewManual.as_view(), name='car_create_manual'),
    path('edit/<int:car_id>', CarEditView.as_view(), name='car_edit'),
    path('delete/<int:car_id>', CarDeleteView.as_view(), name='car_delete'),
    path('list/', CarListView.as_view(), name='car_list'),
]
