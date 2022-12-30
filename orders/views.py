from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

from .forms import CreateOrderForm
from orders.models import Order
from cars.models import Car
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


class CreateOrderView(LoginRequiredMixin, GroupRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating new order.
    """
    template_name = 'orders/order_create.html'
    form_class = CreateOrderForm
    required_group = 'Customer'
    success_url = '/dashboard'

    def get(self, *args, **kwargs):
        date_from_url = f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
        date_from_url = datetime.datetime.strptime(date_from_url, "%Y/%m/%d").date()
        time_from_url = self.kwargs['hour']
        time_from_url = datetime.datetime.strptime(time_from_url, "%H:%M").time()
        
        try:
            garage_opening_hours = OpeningHours.objects.get(garage_id=self.kwargs['garage_id'], weekday=date_from_url.isoweekday())
            if garage_opening_hours.from_hour is None or garage_opening_hours.to_hour is None:
                raise OpeningHours.DoesNotExist
        except OpeningHours.DoesNotExist:
            self.request.messages = messages.error(
                self.request, 'Nie można utworzyć zlecenia. Ten warsztat nie pracuje w wybranym dniu.')
            return redirect('select_date', garage_id=self.kwargs['garage_id'])
        else:
            
            # convert opening hours time to datetime
            opening_hours_from_hour = datetime.datetime.combine(date_from_url, garage_opening_hours.from_hour)
            opening_hours_to_hour = datetime.datetime.combine(date_from_url, garage_opening_hours.to_hour) - datetime.timedelta(hours=1)
            
            def time_in_range(start, end, x):
                """Return true if x is in the range [start, end]"""
                if start <= end:
                    return start <= x <= end
                else:
                    return start <= x or x <= end
                
            test_time = time_in_range(opening_hours_from_hour.time(), opening_hours_to_hour.time(), time_from_url)
                
            if not test_time:
                self.request.messages = messages.error(
                    self.request, 'Nie można utworzyć zlecenia w wybranych godzinach.')
                return redirect('select_date', garage_id=self.kwargs['garage_id'])
            else:
                try:
                    Order.objects.get(date=date_from_url, time=time_from_url, garage=self.kwargs['garage_id'])
                except Order.DoesNotExist:
                    return super().get(self, *args, **kwargs)
                else:
                    self.request.messages = messages.error(
                        self.request, 'Nie można utworzyć zlecenia. Wybrana godzina jest już zajęta.')
                    return redirect('select_date', garage_id=self.kwargs['garage_id'])
                
    def test_func(self):
        return Car.objects.filter(user=self.request.user).exists()
    
    def handle_no_permission(self):
        self.request.messages = messages.error(self.request, 'Nie można utworzyć zlecenia. Nie posiadasz żadnego zarejestrowanego samochodu.')
        return redirect('car_create_select_method')
        
    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CreateOrderView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs
    
    def form_valid(self, form):
        date_from_url = f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
        time_from_url = self.kwargs['hour']
        form.instance.garage_id = self.kwargs['garage_id']
        form.instance.user = self.request.user
        form.instance.time = datetime.datetime.strptime(time_from_url, "%H:%M").time()
        self.request.messages = messages.success(
            self.request, 'Zlecenie zostało utworzone.')
        return super().form_valid(form)
