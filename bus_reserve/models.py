from django.db import models
from uuid import uuid4
from account.models import User

LOCATIONS = (
    ('1', 'Kathmandu'),
    ('2', 'Hetuada'),
    ('3', 'Tandi'),
    ('4', 'Inarwa'),
    ('5', 'Bharatpur'),
    ('6', 'Ithari'),
    ('7', 'Polkhara')
)

t_choices = (
    ('1', 'Completed'),
    ('2', 'Refunded')
)

class Route(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    depart_loc = models.CharField(max_length=20, choices=LOCATIONS, default='1')
    arrive_loc = models.CharField(max_length=20, choices=LOCATIONS, default='1')
    distance = models.IntegerField(default=1)
    price = models.IntegerField(default=100)

class Bus(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    model = models.CharField(max_length=15)
    capacity = models.IntegerField(default=20)
    number_plate = models.CharField(max_length=20)
    image = models.ImageField(upload_to="bus_images/")

class BusSchedule(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bus_id = models.OneToOneField(Bus, on_delete=models.CASCADE)
    depart_date = models.DateTimeField()
    route_id = models.OneToOneField(Route, on_delete=models.CASCADE)

class Seat(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.CharField(max_length=3)
    is_free = models.BooleanField(default=True, blank=True)

class Ticket(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    ticket_num = models.CharField(max_length=10)
    schedule_id = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    seat_id = models.OneToOneField(Seat, on_delete=models.CASCADE)

class TicketOrder(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey('TransactionTable', blank=True,on_delete=models.CASCADE)
    bought_date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1, blank=True)
    ticket_id = models.ManyToManyField(Ticket, blank=True)
   # pending = models.BooleanField(default=True, blank=True, null=True)


class TransactionTable(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, max_length=200)
    t_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=1, blank=True, null=True)
    pidx = models.CharField(max_length=256, blank=True, null=True)
    amount = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=t_choices, default='1')
    khalti_tran_id = models.CharField(max_length=256, blank=True)
    

class TicketHistory(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    cancelled = models.BooleanField(default=False, blank=True)
    refunded = models.BooleanField(default=False, blank=True)
    user_id = models.CharField(max_length=200, blank=True)
    passenger = models.CharField(max_length=30)
    phone = models.IntegerField(default=1, blank=True)
    book_date = models.DateTimeField(blank=True)
    depart_date = models.DateTimeField(blank=True)
    depart_loc = models.CharField(max_length=30, blank=True)
    arrive_loc = models.CharField(max_length=30, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)
    ticket_num = models.CharField(max_length=10, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.RESTRICT, blank=True)
    cost = models.IntegerField(default=1, blank=True)