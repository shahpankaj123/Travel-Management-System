from uuid import uuid4
from django.db import models
from account.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


LOCATIONS = (
    ('1', 'Kathmandu'),
    ('2', 'Hetuada'),
    ('3', 'Tandi'),
    ('4', 'Inarwa'),
    ('5', 'Narayangarh'),
    ('6', 'Ithari'),
    ('7', 'Pokhara'),
    ('8', 'Biratnagar')
)

t_choices = (
    ('1', 'Completed'),
    ('2', 'Refunded'),
    ('3', 'Cancelled')
)

class Route(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    depart_loc = models.CharField(max_length=20, choices=LOCATIONS, default='1')
    arrive_loc = models.CharField(max_length=20, choices=LOCATIONS, default='1')
    distance = models.FloatField(default=1)
    price = models.FloatField(default=100)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return f'{self.get_depart_loc_display()}->{self.get_arrive_loc_display()}'


class Bus(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    model = models.CharField(max_length=15)
    capacity = models.IntegerField(default=20)
    number_plate = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to="bus_images/")

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
    
    def __str__(self):
        return self.model

class BusSchedule(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    depart_date = models.DateTimeField()
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Bus Schedule"
        verbose_name_plural = "Bus Schedules"

    def clean(self):
        
        if self.depart_date < timezone.now():
            raise ValidationError("Cannot set date in past")
        
        # sch = BusSchedule.objects.filter(bus_id=self.bus_id).\
        #     exclude(id=self.id).order_by('-depart_date')

        # if sch:
        #     sch = sch[0]

        #     date_diff = (self.depart_date-sch.depart_date).total_seconds()

        #     if date_diff/3600 < 12:
        #         return ValidationError("Same bus needs 12 hrs difference between schedules")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f' {self.bus_id}--{self.depart_date}'


class Seat(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    bus_id = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Seat"
        verbose_name_plural = "Seats"

    def __str__(self):
        return f'{self.bus_id}->{self.number}'

class Ticket(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    ticket_num = models.CharField(max_length=10)
    schedule_id = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    seat_id = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_bought = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
    
    def __str__(self):
        return self.ticket_num


class TicketOrder(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey('TransactionTable', blank=True,on_delete=models.CASCADE)
    bought_date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1, blank=True)
    ticket_id = models.ManyToManyField(Ticket, blank=True)

    class Meta:
        verbose_name = "Ticket Order"
        verbose_name_plural = "Ticket Orders"

    def __str__(self):
        return str(self.id)

class TransactionTable(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, max_length=200)
    t_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    pidx = models.CharField(max_length=256, blank=True, null=True)
    amount = models.FloatField(default=100)
    status = models.CharField(max_length=20, choices=t_choices, default='1')
    khalti_tran_id = models.CharField(max_length=256, blank=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return self.khalti_tran_id

class TicketHistory(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, blank=True)
    tran_id = models.ForeignKey(TransactionTable, blank=True,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=25, blank=True)
    seat_number = models.CharField(max_length=10, blank=True)
    depart_loc = models.CharField(max_length=25, blank=True)
    arrive_loc = models.CharField(max_length=25, blank=True)
    price = models.FloatField(default=100, blank=True)
    depart_date = models.DateTimeField(blank=True)
    bus_model = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name = "Ticket History"
        verbose_name_plural = "Ticket Histories"
    
    def __str__(self):
        return str(self.id)
