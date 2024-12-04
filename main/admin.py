from django.contrib import admin
from .models import Destination, BoardingLocation, SeatBooking, Seat, Booking
from .models import *
admin.site.register(Destination)
admin.site.register(BoardingLocation)
admin.site.register(SeatBooking)
admin.site.register(Seat)
#admin.site.register(Booking)
from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    def get_seat_number(self, obj):
        return obj.seat.seat_number if obj.seat else "No seat assigned"

    list_display = ['name', 'email', 'get_seat_number', 'fare', 'identification_number']

admin.site.register(Booking, BookingAdmin)

admin.site.register(Driver)
admin.site.register(NonStaff)
admin.site.register(Bus)
admin.site.register(TravelSchedule)
admin.site.site_header='MTN SACCO'
admin.site.site_title='MTN Sacco'
admin.site.index_title='Welcome to MTN Admin Panel'