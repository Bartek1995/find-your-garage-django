from django.contrib import admin

from .models import Order, Expenditure

admin.site.register(Order)
admin.site.register(Expenditure)