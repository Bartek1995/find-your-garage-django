from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.gzip import gzip_page
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from garages.models import Garage
from cars.models import Car
from orders.models import Order, Expenditure

import datetime
from json import dumps
from dateutil.rrule import rrule, MONTHLY


@method_decorator(gzip_page, name='dispatch')
class MainPage(TemplateView):
    """
    Main page view, which is displayed as the main page, when user visits the website.
    """
    
    template_name = 'main/index.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    Based on user type dashboard view, it returns different template.
    """
    
    def get(self, *args, **kwargs):
        if self.request.user.is_customer:
            self.template_name = 'main/dashboard_customer.html'

        elif self.request.user.is_entrepreneur:
            self.template_name = 'main/dashboard_entrepreneur.html'
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        
        # DATA FOR ENTREPRENEUR DASHBOARD
        if self.request.user.is_entrepreneur:
            try:
                context['user_garage'] = Garage.objects.get(user=self.request.user)
            except Garage.DoesNotExist:
                context['user_garage'] = None
            else:
                all_garage_orders = Order.objects.filter(garage=context['user_garage']).order_by('-date', '-time')
                context['waiting_orders_amount'] = all_garage_orders.filter(state=1).count()
                context['accepted_orders_amount'] = all_garage_orders.filter(state=2).count()
                context['in_progress_orders_amount'] = all_garage_orders.filter(state=3).count()
                context['finished_orders_amount'] = all_garage_orders.filter(state=4).count()
                
                this_year_profit = 0
                this_month_profit = 0
                last_orders = []
                last_months_profit = {}
                max_last_orders_counter = 0
    
                # GET LAST 6 MONTHS AND CREATE DICT WITH THEM
                start_date = datetime.date.today().replace(day=15) - datetime.timedelta(days=150)
                for date in rrule(MONTHLY, dtstart=start_date, count=6):
                    last_months_profit[str(date)[:7]] = [str(_(date.strftime("%B"))) + " " + str(date.year), 0]
                    
                # GET ALL EXPENDITURES OF ORDERS AND SUM THEM
                for order in all_garage_orders:
                    this_order_expenditures = Expenditure.objects.filter(order=order, type_of_expenditure="2").aggregate(Sum('price'))['price__sum']
                    
                    if order.date.year == datetime.date.today().year:
                        if this_order_expenditures:
                            this_year_profit += this_order_expenditures
                            
                    if order.date.month == datetime.date.today().month:
                        if this_order_expenditures:
                            this_month_profit += this_order_expenditures

                    # GET MAXIMUM LAST 5 FINISHED ORDERS AND GET THEIR EXPENDITURES
                    if this_order_expenditures and max_last_orders_counter < 5:
                        last_orders.append([str(order.date), str(order.time)[:5], int(this_order_expenditures)])
                        max_last_orders_counter += 1
                    
                    # GET LAST 6 MONTHS PROFIT AND SUM EXPENDITURES OF SELECTED MONTH
                    for key, value in last_months_profit.items():
                        if order.date.strftime("%Y-%m") == key:
                            if this_order_expenditures:
                                last_months_profit[key][1] += int(this_order_expenditures)
                                break
                             
                context['this_year_profit'] = this_year_profit
                context['this_month_profit'] = this_month_profit
                context['last_orders'] = dumps(last_orders)
                context['last_monthly_profits'] = dumps(last_months_profit)
                
        # DATA FOR CUSTOMER DASHBOARD 
        elif self.request.user.is_customer:
            mocked_data = []
            try:
                context['user_cars'] = Car.objects.filter(user=self.request.user)
                if not context['user_cars']:
                    raise Car.DoesNotExist
                
                for car in context['user_cars']:
                    # MOCKING CARS COSTS TO CONSTRUCT CHARTS - IT'S TEMPORARY SOLUTION
                    car.mock_information_about_orders()
                    car_as_dict = car.__dict__
                    del car_as_dict['_state']
                    mocked_data.append(car_as_dict)
                
                for car in mocked_data:
                    for key in car:
                        if isinstance(car[key], datetime.date):
                            car[key] = str(car[key])
                dataJSON = dumps(mocked_data)
                context['user_cars_json'] = dataJSON
                
            except Car.DoesNotExist:
                context['user_cars'] = None
                
        return context
