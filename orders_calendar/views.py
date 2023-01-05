from datetime import datetime, timedelta, date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from django.contrib import messages

from accounts.mixins import GroupRequiredMixin
from orders.models import Order
from garages.models import Garage
from .utils import Calendar
import calendar


class CalendarView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Order
    required_group = "Entrepreneur"
    template_name = 'orders_calendar/calendar.html'

    def get(self, request, *args, **kwargs):
        try:
            self.user_garage = Garage.objects.get(user=self.request.user)
        except Garage.DoesNotExist:
            self.request.messages = messages.warning(self.request, message='Musisz najpierw utworzyć warsztat.')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        # Call the formatmonth method, which returns our calendar as a table
        context['garage_id'] = self.user_garage.id
        html_cal = cal.formatmonth(withyear=True, garage_id=context['garage_id'])
        context['calendar'] = mark_safe(html_cal)
        return context
    
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()