# from django.views.generic import View
from django.views import View
from django.urls import reverse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime
import json


from .models import Bus, BusSchedule, LOCATIONS, Seat, Ticket, TicketOrder


# Create your views here.



class HomeView(View):
    """
    This view is used for landing page. Here user can search for buses

    """
    def get(self, request):
        return render(request, "home.html", {'locations':LOCATIONS})

    def post(self, request):
        depart = request.POST.get('depart')
        arrive = request.POST.get("arrive")
        dep_date = request.POST.get("dep-date")

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

class SeatView(View):

    """
        after user searches for buses they are redirected here
    """

    def get(self, request, scid):
        print(request.user)
        bus_s = BusSchedule.objects.filter(pk=scid)

        if not bus_s:
            return HttpResponse("Invalid url")
        
        bus_id = bus_s[0].bus_id.id

        seats = Seat.objects.filter(bus_id=bus_id)

        return render(request, "seats.html", {'seats':seats})
    
    def post(self, request, scid):
        seat = request.POST.get("seat")
        seat = Seat.objects.get(pk=seat)
        seat.is_free = False
        seat.save()
        ticket = Ticket.objects.get(seat_id=seat)

        # instead of is_bought we can directly check is_free ?
        # ticket.is_bought = True
        # ticket.save()
        tid = ticket.id
        print(tid)
        return redirect(reverse("ticket", kwargs={'tid':tid}))


class BookView(View):
    def get(self, request):
        # ticket = get_object_or_404(Ticket, pk=tid)
        # return render(request, 'book.html', {'ticket':ticket})
        return HttpResponse("All  good")

    def post(self, request):
        seat_ids = request.POST.get('seat_ids')
        seat_ids = json.loads(seat_ids)

        for seat in seat_ids:
            p_name = seat['name']
            p_num = seat['phone']

            st = Seat.objects.get(pk=seat['seat_id'])

            tk = Ticket.objects.get(seat_id=st)
            
            st.is_free = False
            st.save()

            TicketOrder.objects.create(
                user_id = request.user,
                passenger_name = p_name,
                passenger_phone = p_num,
                transaction_id = "sth",
                ticket_id = tk 
            )