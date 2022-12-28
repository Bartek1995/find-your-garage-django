from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CreateOrderForm
from orders.models import Order
from garages.models import OpeningHours
from accounts.mixins import GroupRequiredMixin

import datetime


class SelectDateView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = 'orders/select_date.html'
    required_group = 'Customer'

    def get_queryset(self):
        return Order.objects.filter(garage_id=self.kwargs['garage_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avaliable_days'] = []
        context['garage'] = self.kwargs['garage_id']
        
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=14)

        delta = end_date - start_date

        for loop_date in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=loop_date)
            weekday = day.isoweekday()
            opening_hours = OpeningHours.objects.get(
                garage_id=self.kwargs['garage_id'], weekday=weekday)

            if opening_hours.from_hour is not None or opening_hours.to_hour is not None:
                data_about_day = {
                    'date': day,
                    'weekday': weekday,
                    'opening_hours': opening_hours,
                    'amount_of_available_orders': 0,
                    'amount_of_orders': 0,
                    'avaliable_hours': {},
                }
                
                #  This is the function that rounds the time to the nearest hour
                def hour_rounder(t):
                    time_as_int = int(t.strftime("%H"))
                    temp_time = datetime.datetime.strptime(str(time_as_int), "%H").time()
                    if temp_time < t:
                        time_as_int += 1
                        time_as_int = datetime.datetime.strptime(str(time_as_int), "%H").time()
                        return int(time_as_int.strftime("%H"))
                    else:
                        return int(t.strftime("%H"))
                
                rounded_from_hour = hour_rounder(opening_hours.from_hour)
                
                hours_in_opening_hours_range = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(
                    rounded_from_hour, int(opening_hours.to_hour.strftime("%H")))]

                for hour in hours_in_opening_hours_range:
                    data_about_day['amount_of_orders'] += 1
                    try:
                        Order.objects.get(
                            garage=self.kwargs['garage_id'], date=day, time=hour[0])
                    except Order.DoesNotExist:
                        data_about_day['avaliable_hours'].update(
                            {hour[1]: True})
                        data_about_day['amount_of_available_orders'] += 1
                    else:
                        data_about_day['avaliable_hours'].update(
                            {hour[1]: False})
                        
                if any(value is True for value in data_about_day['avaliable_hours'].values()):
                    context['avaliable_days'].append(data_about_day)
        return context


class CreateOrderView(CreateView):
    """
    View for creating new order.
    """
    template_name = 'orders/order_create.html'
    form_class = CreateOrderForm
    success_url = '/dashboard'

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CreateOrderView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs
    
    def form_valid(self, form):
        date_from_url = f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
        time_from_url = self.kwargs['hour']
        form.instance.garage_id = self.kwargs['garage_id']
        form.instance.user = self.request.user
        form.instance.date = datetime.datetime.strptime(date_from_url, "%Y/%m/%d").date()
        form.instance.time = datetime.datetime.strptime(time_from_url, "%H:%M").time()
        self.request.messages = messages.success(
            self.request, 'Zlecenie zostało utworzone.')
        return super().form_valid(form)
