from django.urls import reverse
import calendar
from orders.models import Order
from django.utils.translation import gettext as _


class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day).order_by('time')
        d = ''
        waiting_orders = 0
        accepted_orders = 0
        in_progress_orders = 0
        finished_orders = 0
        canceled_orders = 0
        
        for event in events_per_day:
            match event.state:
                case 1:
                    waiting_orders += 1
                case 2:
                    accepted_orders += 1
                case 3:
                    in_progress_orders += 1
                case 4:
                    finished_orders += 1
                case 5:
                    canceled_orders += 1
        modal_id = f"modal-{day}"
        if day != 0:
            if events_per_day:
                return f"""
                        <td class="bg-success-subtle">
                            <div class="d-flex flex-column h-100">
                            <span class='date'>{day}</span>
                            { f'<div class="d-flex align-items-center"><div class="waiting-orders dot"></div> {waiting_orders}</div>' if waiting_orders > 0 else ''}
                            { f'<div class="d-flex align-items-center"><div class="accepted-orders dot"></div> {accepted_orders}</div>' if accepted_orders > 0 else ''}
                            { f'<div class="d-flex align-items-center"><div class="in-progress-orders dot"></div> {in_progress_orders}</div>' if in_progress_orders > 0 else ''}
                            { f'<div class="d-flex align-items-center"><div class="finished-orders dot"></div> {finished_orders}</div>' if finished_orders > 0 else ''}
                            { f'<div class="d-flex align-items-center"><div class="bg-danger dot"></div> {canceled_orders}</div>' if canceled_orders > 0 else ''}
                            {self.generate_bootstrap_modal(modal_id=modal_id, list_of_orders=events_per_day)}
                            </div>
                        </td>
                        """
            return f"""
                    <td class="bg-body-secondary">
                    <div class="d-flex flex-column h-100">
                    <span class='date'>{day}</span>
                    </div>
                    </td>
                    """
        else:
            return """
                    <td class="bg-dark-subtle">
                    <div class="d-flex flex-column h-100">
                    </div>
                    </td>
                    """

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'
    
    def get_month_and_year(self):
        month_name = calendar.month_name[self.month]
        translated_month_name = _(month_name)
        return f'<tr><th colspan="7" class="month">{translated_month_name} {self.year}</th></tr>\n'
    
    def formatweekheader(self):
        week_header = ''
        for day in list(calendar.day_abbr):
            week_header += f'<th class="weekday">{_(day)}</th>'
        return f'<tr class="weekday-row"> {week_header} </tr>\n'

    def formatmonth(self, withyear=True, garage_id=None):
        events = Order.objects.filter(garage=garage_id, date__month=self.month)

        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += self.get_month_and_year()
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
    
    def generate_bootstrap_modal(self, modal_id=None, list_of_orders=None, *args, **kwargs):
        list_of_orders_as_li_tags = ""
        for order in list_of_orders:
            list_of_orders_as_li_tags += f"""
            <li class="list-group-item list-group-item-action mb-1">
                <div class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">Nr. #{order.id}</h5>
                  <div class="d-flex flex-column">
                    <small>{ order.date }</small>
                    <small>{ order.time }</small>
                  </div>
                </div>
                <div class="item-body">
                  <div class="item-body__data d-flex align-items-center justify-content-between">
                    <div>
                    <p class="m-1">Status: { order.get_state_as_string }</p>
                    <small>Suma kosztów: 
                    <span class="fw-bold">{ str(order.get_sum_of_expenditures) + " zł</span>" if order.get_sum_of_expenditures is not None else "<span class='fw-bold'>Brak</span>" }</small>
                    </div>

                    <a href="{reverse('manage_order', kwargs={'order_id': order.id})}" class="btn app-btn app-primary-btn"><i class="fa-regular fa-pen-to-square"></i></a>
                  </div>
                </div>
              </li>
            """
        order_list_string = f"""
        <ul class="list-group">
           {list_of_orders_as_li_tags}
        </ul>
        """
        return f""" 
            <button type="button" class="modal-btn align-self-end mt-auto" data-bs-toggle="modal" data-bs-target="#{modal_id}">
            <i class="fa-solid fa-circle-info"></i>
            </button>
            
            <div class="modal fade" id="{modal_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">


            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Lista zleceń</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        {order_list_string}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Zamknij</button>
                    </div>
                </div>
            </div>
        </div>
        """
    