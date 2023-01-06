from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.shortcuts import redirect

from .forms import CreateOrderForm, ChangeOrderStateForm
from orders.models import Order, Expenditure
from cars.models import Car
from garages.models import Garage
from garages.models import OpeningHours
from accounts.mixins import GroupRequiredMixin

import datetime


class SelectDateView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """
    View for selecting date and time for new order.
    """
    
    template_name = 'orders/select_date.html'
    required_group = 'Customer'

    def get_queryset(self):
        return Order.objects.filter(garage_id=self.kwargs['garage_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avaliable_days'] = []
        context['garage'] = self.kwargs['garage_id']
        
        start_date = datetime.date.today() + datetime.timedelta(days=1)
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
                
                hours_in_opening_hours_range = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(
                    int(opening_hours.from_hour.strftime("%H")), int(opening_hours.to_hour.strftime("%H")))]

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
    date_from_url = None
    time_from_url = None
        
    def get(self, *args, **kwargs):
        self.init_date_and_time_from_url()
        try:
            garage_opening_hours = OpeningHours.objects.get(garage_id=self.kwargs['garage_id'], weekday=self.date_from_url.isoweekday())
            if garage_opening_hours.from_hour is None or garage_opening_hours.to_hour is None:
                raise OpeningHours.DoesNotExist
        except OpeningHours.DoesNotExist:
            self.request.messages = messages.error(
                self.request, 'Nie można utworzyć zlecenia. Ten warsztat nie pracuje w wybranym dniu.')
            return redirect('select_date', garage_id=self.kwargs['garage_id'])
        else:
            
            # convert opening hours time to datetime
            opening_hours_from_hour = datetime.datetime.combine(self.date_from_url, garage_opening_hours.from_hour)
            opening_hours_to_hour = datetime.datetime.combine(self.date_from_url, garage_opening_hours.to_hour) - datetime.timedelta(hours=1)
            
            def time_in_range(start, end, x):
                """Return true if x is in the range [start, end]"""
                if start <= end:
                    return start <= x <= end
                else:
                    return start <= x or x <= end
                
            test_time = time_in_range(opening_hours_from_hour.time(), opening_hours_to_hour.time(), self.time_from_url)
                
            if not test_time:
                self.request.messages = messages.error(
                    self.request, 'Nie można utworzyć zlecenia w wybranych godzinach.')
                return redirect('select_date', garage_id=self.kwargs['garage_id'])
            else:
                if self.check_time_from_url():
                    return super().get(*args, **kwargs)
                return redirect('select_date', garage_id=self.kwargs['garage_id'])
    
    def post(self, request, *args, **kwargs):
        if self.check_time_from_url():
            return super().post(request, *args, **kwargs)
        return redirect('select_date', garage_id=self.kwargs['garage_id'])
        
    def test_func(self):
        return Car.objects.filter(user=self.request.user).exists()
    
    def init_date_and_time_from_url(self):
        self.date_from_url = f"{self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}"
        self.date_from_url = datetime.datetime.strptime(self.date_from_url, "%Y/%m/%d").date()
        self.time_from_url = self.kwargs['hour']
        self.time_from_url = datetime.datetime.strptime(self.time_from_url, "%H:%M").time()
        
    def handle_no_permission(self):
        self.request.messages = messages.error(self.request, 'Nie można utworzyć zlecenia. Nie posiadasz żadnego zarejestrowanego samochodu.')
        return redirect('car_create_select_method')
        
    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CreateOrderView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garage'] = Garage.objects.get(id=self.kwargs['garage_id'])
        context['date'] = self.date_from_url
        context['time'] = self.time_from_url
        return context
        
    def check_time_from_url(self):
        """
        Function check if time from url is avaliable to create order.
        """
        self.init_date_and_time_from_url()
        try:
            Order.objects.get(date=self.date_from_url, time=self.time_from_url, garage=self.kwargs['garage_id'])
        except Order.DoesNotExist:
            return True
        self.request.messages = messages.error(
            self.request, 'Nie można utworzyć zlecenia. W wybranym terminie jest już zarezerwowane zlecenie.')
        return False
    
    def form_valid(self, form):
        form.instance.garage_id = self.kwargs['garage_id']
        form.instance.user = self.request.user
        form.instance.time = self.time_from_url
        form.instance.date = self.date_from_url
        self.request.messages = messages.success(
            self.request, 'Zlecenie zostało utworzone.')
        return super().form_valid(form)


class HistoryOfOrdersView(LoginRequiredMixin, ListView):
    """
    View for showing order history.
    """
    template_name = 'orders/history_of_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_customer:
            return Order.objects.filter(user=self.request.user).order_by('-date', '-time')
        else:
            user_garage = Garage.objects.get(user=self.request.user)
            return Order.objects.filter(garage=user_garage).order_by('-created')
        
        
class ActiveOrdersView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    """
    View for showing active orders.
    """
    template_name = 'orders/active_orders.html'
    context_object_name = 'orders'
    required_group = 'Customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['waiting_orders'] = Order.objects.filter(state=1, user=self.request.user).order_by('date', 'time')
        context['accepted_orders'] = Order.objects.filter(state=2, user=self.request.user).order_by('date', 'time')
        context['in_progress_orders'] = Order.objects.filter(state=3, user=self.request.user).order_by('date', 'time')
        context['finished_orders'] = Order.objects.filter(state=4, user=self.request.user).order_by('date', 'time')
        context['rejected_orders'] = Order.objects.filter(state=5, user=self.request.user).order_by('date', 'time')
        return context
    
    
class ManageOrderView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/order_management.html'
    form_class = ChangeOrderStateForm
    
    def get(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            if self.request.user.is_customer and order.user != self.request.user:
                self.request.messages = messages.error(self.request, 'Nie jesteś właścicielem tego zlecenia.')
                return redirect('dashboard')
        except Order.DoesNotExist:
            self.request.messages = messages.error(self.request, 'Nie można znaleźć zlecenia.')
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.request.path

    def get_object(self):
        return Order.objects.get(id=self.kwargs['order_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenditures'] = Expenditure.objects.filter(order=self.kwargs['order_id'])
        return context
    
    def form_valid(self, form):
        self.request.messages = messages.success(self.request, 'Status zlecenia został zaktualizowany.')
        return super().form_valid(form)