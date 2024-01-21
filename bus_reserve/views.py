# from django.views.generic import View
from django.views import View
from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime
import json

import string
from random import choices

from .models import Bus, BusSchedule, LOCATIONS, Seat #Ticket


def get_ticket_num():
    chars = string.ascii_uppercase
    nums = string.digits
    val = choices(chars, k=4)
    val =  val+choices(nums, k=4)

    return ''.join(val)

# Create your views here.



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
        
        bus_id = bus_s.bus_id.id

        seats = Seat.objects.filter(bus_id=bus_id)

        return render(request, "book_bus.html", {'seats':seats})
    
    def post(self, request, bsid):
        seats = json.loads(request.body.decode('UTF-8'))

        for sid in seats['selectedSeats']:
            tik = Seat.objects.get(pk=sid)

            tik.is_free = False
            tik.save()

        print(seats)
        return HttpResponse("lol")


# class BookView(View):
#     def get(self, request):
#         # ticket = get_object_or_404(Ticket, pk=tid)
#         # return render(request, 'book.html', {'ticket':ticket})
#         return HttpResponse("All  good")

#     def post(self, request):
#         seat_ids = request.POST.get('seat_ids')
#         seat_ids = json.loads(seat_ids)

#         for seat in seat_ids:
#             p_name = seat['name']
#             p_num = seat['phone']

#             st = Seat.objects.get(pk=seat['seat_id'])

#             tk = Ticket.objects.get(seat_id=st)
            
#             st.is_free = False
#             st.save()

#             TicketOrder.objects.create(
#                 user_id = request.user,
#                 passenger_name = p_name,
#                 passenger_phone = p_num,
#                 transaction_id = "sth",
#                 ticket_id = tk 
#             )
    