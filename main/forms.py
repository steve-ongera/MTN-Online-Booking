from django import forms
from .models import SeatBooking

class SeatBookingForm(forms.ModelForm):
    class Meta:
        model = SeatBooking
        fields = ['name', 'email', 'phone', 'destination', 'boarding_location', 'seats']