from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.db import models
from django.utils.crypto import get_random_string
#from .signals import create_seats_for_schedule



class Destination(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BoardingLocation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=50)
    identification = models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
       return self.name

class Bus(models.Model):
    name = models.CharField(max_length=50)
    plate_number=models.CharField(max_length=50 , unique=True)
    route = models.CharField(max_length=50)
    Driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_in_good = models.BooleanField(default=True)
    timeoftravel = models.CharField(max_length=50)
    fare = models.CharField(max_length=50)
   
    def __str__(self):
       return f'{self.name} - {self.plate_number}'


class TravelSchedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    boarding_location = models.ForeignKey(BoardingLocation, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    date_of_travel = models.DateField()
    departure_time = models.TimeField()
    fare = models.CharField(max_length=50 , null=True , blank=True)

    def __str__(self):
        return f"{self.bus.name} | {self.boarding_location.name} -> {self.destination.name} on {self.date_of_travel}"



    
class Seat(models.Model):
    bus_schedule = models.ForeignKey(
        TravelSchedule, on_delete=models.CASCADE, null=True, blank=True
    )
    seat_number = models.CharField(max_length=5)
    is_reserved = models.BooleanField(default=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)  # Link seat to bus
    reservation_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
          bus_name = self.bus.name if self.bus else "No Bus Assigned"
          return f"Seat: {self.seat_number} (Bus: {bus_name}, Reserved: {self.is_reserved})"


    
class Booking(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=10 , decimal_places=2)
    identification_number = models.CharField(max_length=50)
    booking_order_id = models.CharField(max_length=12, unique=True, blank=True, null=True)  # New field

    def generate_booking_order_id(self):
        """Generates a unique alphanumeric booking order ID."""
        characters = string.ascii_uppercase + string.digits
        booking_id = ''.join(random.choices(characters, k=8))  # generates 8-character ID
        return booking_id

    def save(self, *args, **kwargs):
        if not self.booking_order_id:  # Generate the booking ID only if not already set
            self.booking_order_id = self.generate_booking_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        # Check if seat is assigned and if it has the necessary attributes
        seat_number = self.seat.seat_number if self.seat and self.seat.seat_number else "No seat assigned"
        return f"{self.name} - {self.email}: Seat number --> {seat_number}"

        

class NonStaff(models.Model):
    name = models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    identification = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
       return self.name
    


