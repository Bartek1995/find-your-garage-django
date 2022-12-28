from django.urls import path
from .views import CreateOrderView, SelectDateView


urlpatterns = [
    path('create/<int:garage_id>/<int:year>/<int:month>/<int:day>/<str:hour>', CreateOrderView.as_view(), name='create_order'),
    path('select_date/<int:garage_id>', SelectDateView.as_view(), name='select_date'),

]
