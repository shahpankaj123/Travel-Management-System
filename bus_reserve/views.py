#external
import json
import string
import requests
from uuid import uuid4
from random import choices
from datetime import datetime

#django
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

#internal
from .models import (
    Bus,
    BusSchedule,
    LOCATIONS,
    Seat, 
    Ticket,
    TicketHistory,
    TicketOrder,
    TransactionTable)

def get_ticket_num():
    chars = string.ascii_uppercase
    nums = string.digits
    val = choices(chars, k=4)
    val =  val+choices(nums, k=4)

    return ''.join(val)

# Create your views here.


def get_details(request):
    username = request.user.username
    #phone = request.user.ph
    email = request.user.email
    cur_path = request.get_full_path()
    phone = '9800000000'
    return username, phone, email, cur_path, str(uuid4())

class HomeView(View):
    """
    This view is used for landing page. Here user can search for buses

    """
    def get(self, request):
        return render(request, "index.html", {'locations':LOCATIONS})

    def post(self, request):
        depart = request.POST.get('depart')
        arrive = request.POST.get("arrive")
        dep_date = request.POST.get("dep-date")

        return redirect(f"/buses/?depart={depart}&arrive={arrive}&dep-date={dep_date}")
    
class BusesView(View):

    def get(self, request):
        depart = request.GET.get('depart')
        arrive = request.GET.get("arrive")
        dep_date = request.GET.get("dep-date")

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

        return render(request, 'buses.html', {'buses':buses})


class BookView(View):
    def get(self, request, bsid):
        if "favicon.png" in request.path:
            return HttpResponse(status=204)
        
        bus_s = get_object_or_404(BusSchedule, pk=bsid)
    

        tickets = Ticket.objects.filter(schedule_id=bus_s)

        tickets = [(tickets[i], tickets[i+1]) for i in range(0, len(tickets)-1, 2)]

        return render(request, "book_bus.html", {'tickets':tickets})
    
    def post(self, request, bsid):
        tickets = json.loads(request.body.decode('UTF-8'))

        with open("static/json/purchase_detail.json", "r") as f:
            purchase_detail = json.load(f)

        qty = len(tickets['selectedSeats'])

        tik = Ticket.objects.get(pk=tickets['selectedSeats'][0])

        price = tik.schedule_id.route_id.price

        username, phone, email, cur_path, t_id \
            = get_details(request)

        purchase_detail['return_url'] = purchase_detail['website_url']+cur_path
        purchase_detail['customer_info']['name'] = username
        purchase_detail['customer_info']['email'] = email
        purchase_detail['customer_info']['phone'] = phone

        purchase_detail['purchase_order_id'] = t_id
        purchase_detail['amount'] = price*qty*100
        
        purchase_detail['product_details'][0]['total_price'] = price*qty
        purchase_detail['product_details'][0]['quantity'] = qty
        purchase_detail['product_details'][0]['unit_price'] = price
        

        headers = {
                'Authorization': 'key 628f4ebcb93e41528b80678beea2ec83',
                'Content-Type': 'application/json',
        }
        
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        
        resp = requests.post(url, headers=headers, data=json.dumps(purchase_detail))

        resp_j = resp.json()
        print(resp_j)
        return redirect(resp_j['payment_url'])
 
        # to be replaced with actual transcation id
        # t = TransactionTable(pk='b40f4678-676a-4e28-892d-389715453981')
        
        # tik_h = TicketOrder.objects.create(
        #     transaction_id = t,
        #     user_id = request.user,
        #     quantity = len(seats['selectedSeats'])
        # )
        # tik_h.save()

        # for sid in seats['selectedSeats']:
        #     tik = Ticket.objects.get(seat_id=sid)
        #     tik.seat_id.is_free = False
        #     tik.seat_id.save()
        #     tik_h.ticket_id.add(tik)
        #     tik.save()

class ConfirmView(View):
    def get(self, request):
        return render()