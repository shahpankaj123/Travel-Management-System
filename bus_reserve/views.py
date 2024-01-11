from django.shortcuts import render
from .models import Bus, BusSchedule, LOCATIONS

from datetime import datetime



# Create your views here.

def home(request):
    if request.method == 'POST':
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
    
    else:
        return render(request, "home.html", {'locations':LOCATIONS})
