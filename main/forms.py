from django import forms
from .models import SeatBooking

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

