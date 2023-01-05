from django.urls import path
from .views import CalendarView


urlpatterns = [
    path('<int:garage_id>/calendar', CalendarView.as_view(), name='calendar'),
]
