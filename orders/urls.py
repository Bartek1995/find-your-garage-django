from django.urls import path
from .views import CreateOrderView, SelectDateView, HistoryOfOrdersView, ActiveOrdersView


urlpatterns = [
    path('create/<int:garage_id>/<int:year>/<int:month>/<int:day>/<str:hour>', CreateOrderView.as_view(), name='create_order'),
    path('select_date/<int:garage_id>', SelectDateView.as_view(), name='select_date'),
    path('history', HistoryOfOrdersView.as_view(), name='history_of_orders'),
    path('active', ActiveOrdersView.as_view(), name='active_orders'),

]
