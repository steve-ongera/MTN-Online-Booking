from django.contrib import admin
from .models import Destination, BoardingLocation,  Seat, Booking
from .models import *
admin.site.register(Destination)
admin.site.register(BoardingLocation)
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
admin.site.site_header='mtn sacco'
admin.site.site_title='mtn sacco '
admin.site.index_title='mtn sacco | 2024 '