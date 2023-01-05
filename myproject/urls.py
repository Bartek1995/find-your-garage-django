from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    path('garage/', include('garages.urls')),
    path('car/', include('cars.urls')),
    path('order/', include('orders.urls')),
    path('order/', include('orders_calendar.urls'))
]
