import json
import string
from random import choices
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import (
    Bus,
    BusSchedule,
    Seat,
    Ticket,
    TicketOrder,
    TicketHistory
)

def get_ticket_num():
    chars = string.ascii_uppercase
    nums = string.digits
    val = choices(chars, k=4)
    val =  val+choices(nums, k=4)

    return ''.join(val)

@receiver(post_save, sender=Bus)
def populate(sender, instance=None, created=False, **kwargs):
    if created:
        capacity = instance.capacity
        
        cap_a = 65
        seats = []
        for _ in range(int(capacity/2)):
            for j in ['1', '2']:
                seats.append(Seat(bus_id=instance, number=chr(cap_a)+j))
            cap_a += 1
        
        Seat.objects.bulk_create(seats)

@receiver(pre_delete)
def clean_images(sender, instance=None, **kwargs):
    if hasattr(instance, 'image'):
        instance.image.delete(False)


@receiver(post_save, sender=BusSchedule)
def populate_tickets(sender, instance=None, created=False, **kwargs):
    if created:
        seats = Seat.objects.filter(bus_id=instance.bus_id)

        Ticket.objects.bulk_create(
            [Ticket(ticket_num=get_ticket_num(),
                   schedule_id=instance,
                   seat_id=seat
                ) for seat in seats]
        )

        interval_schedule = IntervalSchedule.objects.create(
                                                    every=365,
                                                    period=IntervalSchedule.DAYS
                                                )
        
        PeriodicTask.objects.create(name=str(instance.id),
                                    task='remove_schedule',
                                    interval=interval_schedule,
                                    args=json.dumps([str(instance.id)]),
                                    start_time=instance.depart_date
                                )

@receiver(pre_delete, sender=BusSchedule)
def populate_ticket_history(sender, instance=None, created=False, **kwargs):
    tik_ords = TicketOrder.objects.filter(ticket_id__schedule_id=instance.id\
                                         ).distinct()
    
    depart_loc = instance.route_id.depart_loc
    arrive_loc = instance.route_id.arrive_loc
    depart_d = instance.depart_date
    bus_model = instance.bus_id.model

    for tik_ord in tik_ords:
        
        price = tik_ord.transaction_id.amount/tik_ord.quantity

        for tik in tik_ord.ticket_id.all():
            tik.seat_id.is_free=True
            tik.seat_id.save()

        TicketHistory.objects.bulk_create([TicketHistory(
            tran_id = tik_ord.transaction_id,
            user_id = tik_ord.user_id,
            ticket_number = tik.ticket_num,
            seat_number = tik.seat_id.number,
            depart_loc=depart_loc,
            arrive_loc=arrive_loc,
            price = price,
            depart_date = depart_d,
            bus_model = bus_model) for tik in tik_ord.ticket_id.all()]
        )
        tik_ord.delete()
    
    