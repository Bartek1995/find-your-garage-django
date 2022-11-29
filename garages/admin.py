from django.contrib import admin
from .models import Garage, ServiceList, OpeningHours

admin.site.register(Garage)
admin.site.register(ServiceList)
admin.site.register(OpeningHours)