from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from random import choices
import string

from .models import (
    Bus,
    BusSchedule,
    Seat
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

        for _ in range(int(capacity/2)):
            for j in ['1', '2']:
                ins = Seat(bus_id=instance, number=chr(cap_a)+j)
                print(ins.id)
                print(ins.number)
                ins.save()
            cap_a += 1

@receiver(pre_delete)
def clean_images(sender, instance=None, **kwargs):
    if hasattr(instance, 'image'):
        instance.image.delete(False)


# @receiver(post_save, sender=BusSchedule)
# def populate_tickets(sender, instance=None, created=False, **kwargs):
#     if created:
#         seats = Seat.objects.filter(bus_id=instance.bus_id)

#         for seat in seats:
#             ins = Ticket(ticket_num=get_ticket_num(), schedule_id=instance, seat_id=seat)
#             ins.save()

