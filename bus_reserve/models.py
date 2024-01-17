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

# status = (
#     ('Booked', 'Booked'),
#     ('Cancelled', 'Cancelled'),
#     ('Refunded', 'Refunded')
# )

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
    datetime = models.DateTimeField()
    route_id = models.OneToOneField(Route, on_delete=models.CASCADE)

class Seat(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.CharField(max_length=3)
    is_free = models.BooleanField(default=True, blank=True)

class Ticket(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    ticket_num = models.CharField(max_length=10)
    #is_bought = models.BooleanField(default=False, blank=True)
    schedule_id = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    seat_id = models.OneToOneField(Seat, on_delete=models.CASCADE)

class TicketOrder(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bought_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  #  passenger_name = models.CharField(max_length=60, blank=True)
  #  passenger_phone = models.IntegerField(default=1)
    transaction_id = models.ForeignKey('TransactionTable', default="Refunded", on_delete=models.SET_DEFAULT)
    ticket_id = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    
class TransactionTable(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, blank=True, max_length=200)
    t_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)

# class DepartInfo(models.Model):
#     id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
#     passenger_arrived = models.BooleanField(default=False)
#     ticket_order_id = models.ForeignKey(TicketOrder, on_delete=models.CASCADE)
#     bus_problem = models.BooleanField(default=False)

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

    #ticket_order_id = models.ForeignKey(TicketOrder, on_delete=models.CASCADE)

