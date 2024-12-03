from django.contrib import admin
from .models import Destination, BoardingLocation, SeatBooking, Seat, Booking
from .models import *
admin.site.register(Destination)
admin.site.register(BoardingLocation)
admin.site.register(SeatBooking)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Driver)
admin.site.register(NonStaff)
admin.site.register(Bus)
admin.site.site_header='MTN SACCO'
admin.site.site_title='MTN Sacco'
admin.site.index_title='Welcome to MTN Admin Panel'