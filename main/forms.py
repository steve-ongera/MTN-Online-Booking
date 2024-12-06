from django import forms
from .models import *

class SeatBookingForm(forms.ModelForm):
    class Meta:
        model = SeatBooking
        fields = ['name', 'email', 'phone', 'destination', 'boarding_location', 'seats']




from django import forms
from .models import BoardingLocation, Destination
from datetime import date

class TravelScheduleSearchForm(forms.Form):
    boarding_location = forms.ModelChoiceField(queryset=BoardingLocation.objects.all(), required=True)
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), required=True)
    date_of_travel = forms.DateField(initial=date.today, widget=forms.SelectDateWidget(empty_label=("Choose year", "Choose month", "Choose day")))



class TravelScheduleForm(forms.ModelForm):
    class Meta:
        model = TravelSchedule
        fields = ['bus', 'boarding_location', 'destination', 'date_of_travel', 'departure_time', 'fare']


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'plate_number', 'route', 'Driver', 'is_in_good', 'timeoftravel', 'fare']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'identification', 'email', 'gender', 'mobile', 'address']


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name']

class BoardingLocationForm(forms.ModelForm):
    class Meta:
        model = BoardingLocation
        fields = ['name']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat', 'name', 'email', 'phone', 'fare', 'identification_number']


class NonStaffForm(forms.ModelForm):
    class Meta:
        model = NonStaff
        fields = ['name', 'email', 'identification', 'gender', 'mobile', 'address']