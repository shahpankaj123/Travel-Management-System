from django.db import models
from account.models import User

class Bus(models.Model):
    bus_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField(null=True, blank=True)
    # Add other bus details

class BusSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    # Add other schedule details

class Booking(models.Model):
    user_profile = models.ForeignKey(User,on_delete=models.CASCADE)
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')
    booking_time = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    seat_numbers = models.CommaSeparatedIntegerField(max_length=255)

    def save(self, *args, **kwargs):
        # Check if the selected seats are already booked for this schedule
        booked_seats = Booking.objects.filter(bus_schedule=self.bus_schedule)
        booked_seat_numbers = [seat for booking in booked_seats for seat in booking.seat_numbers.split(',')]
        
        # Check for seat number conflicts
        if any(seat in booked_seat_numbers for seat in self.seat_numbers.split(',')):
            raise ValueError("One or more selected seats are already booked for this schedule.")
        
        # If no conflicts, proceed with the booking
        super().save(*args, **kwargs)

class Refund(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    processed_time = models.DateTimeField(auto_now_add=True)
    # Add other refund details



class Review(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    bus_schedule = models.ForeignKey(BusSchedule, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_time = models.DateTimeField(auto_now_add=True)
    # Add other review details

class Notification(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_time = models.DateTimeField(auto_now_add=True)
    # Add other notification details
