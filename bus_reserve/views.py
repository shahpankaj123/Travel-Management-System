# from django.views.generic import View
from django.views import View

from django.shortcuts import render, HttpResponse
from datetime import datetime

from .models import Bus, BusSchedule, LOCATIONS, Seat


# Create your views here.

class HomeView(View):

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

    def get(self, request, scid):
        bus_s = BusSchedule.objects.filter(pk=scid)

        if not bus_s:
            return HttpResponse("Invalid url")
        
        bus_id = bus_s[0].bus_id.id

        seats = Seat.objects.filter(bus_id=bus_id)

        return render(request, "seats.html", {'seats':seats})
    
# class BookView(View):
#     def get()