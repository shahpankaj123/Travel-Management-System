from uuid import UUID
from celery import shared_task
from .models import BusSchedule

@shared_task(name="remove_schedule")
def remove_schedule(bs_id):
    bs = BusSchedule.objects.get(pk=UUID(bs_id))
    bs.delete()
    print("Schedule deleted")