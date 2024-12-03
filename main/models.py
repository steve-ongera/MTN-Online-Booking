from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class BoardingLocation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SeatBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    boarding_location = models.ForeignKey(BoardingLocation, on_delete=models.CASCADE)
    seats = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {', '.join(self.seats.split(','))}"
    
class Seat(models.Model):
    seat_number = models.CharField(max_length=5, unique=True)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number
    
class Booking(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    fare = models.DecimalField(max_digits=10 , decimal_places=2)
    identification_number=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}--  {self.email} :  seat number ------> {self.seat.seat_number}"
    
class Driver(models.Model):
    name = models.CharField(max_length=50)
    identification = models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
       return self.name
    
class NonStaff(models.Model):
    name = models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    identification = models.CharField(max_length=50)
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