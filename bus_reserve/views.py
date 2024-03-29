#external
import json
from django.http.response import HttpResponse as HttpResponse
import requests
from uuid import uuid4
from decouple import config
from datetime import datetime


#django
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden

#internal
from account.tasks import Send_ticket
from .models import BusSchedule, LOCATIONS, Ticket, TicketOrder, TransactionTable, Seat, Route

k_api = config('KHALTI')

headers = {
        'Authorization': f'key {k_api}',
        'Content-Type': 'application/json',
}

# adds transaction details and books a ticket
def add_ticket_order(request, tickets, pidx, p_id):

    k_t_id = request.GET.get('transaction_id')
    amount = float(request.GET.get('amount'))/100
    mobile = request.GET.get('mobile')
    user_id = request.user
    qty = len(tickets)

    t_id = TransactionTable.objects.create(
                                            pk=p_id,
                                            pidx=pidx,
                                            user_id=user_id,
                                            khalti_tran_id=k_t_id,
                                            amount=amount,
                                            phone=mobile
                                        )

    tik = TicketOrder.objects.create(
        user_id = user_id,
        quantity = qty,
        transaction_id = t_id,
    )
    
    tik.save()

    tik_obj = Ticket.objects.filter(pk__in=tickets)
    
    for ticket in tik_obj:
        tik.ticket_id.add(ticket)
        ticket.is_bought = True
        ticket.save()

# generates payload to post to khalti server
def get_khalti_payload(request, price, qty):

    username = request.user.username
    email = request.user.email
    cur_path = request.get_full_path()
    phone = request.user.ph
    t_id = uuid4()
    uri = request.build_absolute_uri("/")[:-1]

    with open("static/json/purchase_detail.json", "r") as f:
        purchase_detail = json.load(f)

    purchase_detail['website_url'] = uri
    purchase_detail['return_url'] = uri+cur_path

    purchase_detail['customer_info']['name'] = username
    purchase_detail['customer_info']['email'] = email
    purchase_detail['customer_info']['phone'] = phone
    
    purchase_detail['purchase_order_id'] = str(t_id)
    purchase_detail['amount'] = price*qty*100
    
    purchase_detail['product_details'][0]['total_price'] = price*qty
    purchase_detail['product_details'][0]['quantity'] = qty
    purchase_detail['product_details'][0]['unit_price'] = price

    print(purchase_detail)

    return purchase_detail

class HomeView(View):
    """
    This view is used for landing page. Here user can search for buses

    """
    def get(self, request):
        routes = BusSchedule.objects.all()

        arrive_locs = set([(bs.route_id.arrive_loc, bs.route_id.get_arrive_loc_display()) for bs in routes])
        depart_locs = set([(bs.route_id.depart_loc, bs.route_id.get_depart_loc_display()) for bs in routes])


        return render(request, "index.html", {'arrive_loc':arrive_locs, 'depart_loc':depart_locs})

    def post(self, request):
        depart = request.POST.get('depart')
        arrive = request.POST.get("arrive")
        dep_date = request.POST.get("dep-date")

        return redirect(f"/buses/?depart={depart}&arrive={arrive}&dep-date={dep_date}")
    
class BusesView(View):
    """
        This view shows info about all the scheduled buses
    """

    def get(self, request):
        depart = request.GET.get('depart')
        arrive = request.GET.get("arrive")
        dep_date = request.GET.get("dep-date")

        # depart date is optional for searching
        if dep_date:

            dep_date = datetime.strptime(dep_date, '%Y-%m-%d').date()

            buses = BusSchedule.objects.filter(
                depart_date__date=dep_date,
                route_id__arrive_loc=arrive,
                route_id__depart_loc=depart
                ).select_related('bus_id', 'route_id')
        else:
            buses = BusSchedule.objects.filter(
                route_id__arrive_loc=arrive,
                route_id__depart_loc=depart).select_related('bus_id', 'route_id')
        
        seats = []
        
        for bus in buses:
            reserved = Ticket.objects.filter(schedule_id=bus.id, is_bought=True).count()
            seats.append(bus.bus_id.capacity-reserved)
            
        return render(request, 'buses.html', {'buses':zip(buses, seats)})



class BookView(View):
    """
        Here user can books seats in bus.
        In the initial get method the user can see all the available seats and select at least one
        and at most 4 seats and submit it where they will eb redirected to khalti website.
        After confirming the payment in the get method their purchase will eb successful and they
        can further book more seats
    """
    login_url = '/user/Login/'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and self.request.method == 'POST':
            return JsonResponse({"login_url":self.login_url}, status=403)
        
        return super().dispatch(request, *args, **kwargs)

    # def handle_no_permission(self):
    #     if self.request.method == 'POST':
    #         return JsonResponse({"login_url":self.login_url}, status=403)
    #     return super().handle_no_permission()

    def get(self, request, bsid):
        if "favicon.png" in request.path:
            return HttpResponse(status=204)
        
        pidx = request.GET.get('pidx')
        purchase_order_id = request.GET.get('purchase_order_id')

        bus_s = get_object_or_404(BusSchedule, pk=bsid)

        diff = bus_s.depart_date - timezone.now()


        # if diff.total_seconds()/60<15:
        #     return HttpResponse("Bus already boarded")
       
        if pidx:
            resp = requests.post(
                                    "https://a.khalti.com/api/v2/epayment/lookup/",
                                    headers=headers,
                                    data=json.dumps({'pidx':pidx}),
                                ).json()
            
            tickets = request.session.get('tickets')

            if 'detail' in resp:
                return HttpResponse(resp['detail'])

            elif not TransactionTable.objects.filter(pk=purchase_order_id) and resp['status']=='Completed':
                add_ticket_order(request, tickets, pidx, purchase_order_id)

            #    orders = TicketOrder.objects.filter(user_id=request.user)
                
                rq = [request.user.email, bsid]

                Send_ticket.delay(rq)

                messages.success(request, "Ticket booked check your email for invoice")
        
        tickets = Ticket.objects.filter(schedule_id=bus_s)

        tickets = [(tickets[i], tickets[i+1])\
                   for i in range(0, len(tickets)-1, 2)]

        return render(request, "book_bus.html", {'tickets':tickets})
    
    def post(self, request, bsid):
        tickets = json.loads(request.body.decode('UTF-8'))['selectedSeats']
        qty = len(tickets)
        db_qty = len(TicketOrder.objects.filter(user_id=request.user, ticket_id__schedule_id=bsid))

        if not db_qty:
            db_qty = 0

        if qty > 4 or db_qty+qty>4:
            return JsonResponse({'message':'max seats booked'})
        
        request.session['tickets'] = tickets

        tik = Ticket.objects.get(pk=tickets[0])

        price = tik.schedule_id.route_id.price        
        
        url = "https://a.khalti.com/api/v2/epayment/initiate/"



        purchase_detail = get_khalti_payload(request, price, qty)
        
        resp = requests.post(url, headers=headers, data=json.dumps(purchase_detail)).json()

        print(resp)

        return JsonResponse(resp)

