
from django.shortcuts import render, redirect 
from .models import Destination, BoardingLocation , Seat
from .forms import SeatBookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from .models import Seat, Booking
from .models import *
# for user authticcation 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin,logout
from django.shortcuts import get_object_or_404, render


@csrf_exempt
def confirm_booking(request, bus_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        fare = request.POST.get('fare')
        identification_number = request.POST.get('identification_number')

        try:
            seat = Seat.objects.get(seat_number=seat_number, bus_id=bus_id)
            if seat.is_reserved:
                messages.error(request, "The seat is already booked.")
                return redirect('seat_reservation', bus_id=bus_id)

            # Save the booking
            Booking.objects.create(
                seat=seat,
                name=name,
                email=email,
                phone=phone,
                fare=fare,
                identification_number=identification_number,
            )

            # Mark the seat as reserved
            seat.is_reserved = True
            seat.save()
            messages.success(request, "Booking successful! You will receive your ticket via email.")
            return redirect('success')

        except Seat.DoesNotExist:
            messages.error(request, "Invalid seat selection.")
            return redirect('seat_reservation', bus_id=bus_id)

    return redirect('seat_reservation', bus_id=bus_id)


from django.utils import timezone
def book_seats(request, bus_id):
    seat_number = request.GET.get('seat')

    if not seat_number:
        messages.error(request, "Please select a seat.")
        return redirect('seat_reservation', bus_id=bus_id)

    try:
        seat = Seat.objects.get(seat_number=seat_number, bus_id=bus_id)
        if seat.is_reserved:
            messages.error(request, "The seat you selected is already booked!")
            return redirect('seat_reservation', bus_id=bus_id)
    except Seat.DoesNotExist:
        messages.error(request, "The selected seat does not exist for this bus.")
        return redirect('seat_reservation', bus_id=bus_id)

    # If the user submits the booking form
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        identification_number = request.POST.get('identification_number')
        fare = 300  # The fare can be dynamically calculated based on the destination

        # Mark the seat as reserved
        seat.is_reserved = True
        seat.reservation_time = timezone.now()
        seat.save()

        # Create a Booking record
        booking = Booking.objects.create(
            seat=seat,
            name=name,
            email=email,
            phone=phone,
            fare=fare,
            identification_number=identification_number
        )

        # Redirect to a payment confirmation page or show a success message
        messages.success(request, f"Booking confirmed for seat {seat.seat_number}. Please proceed with payment.")
        return redirect('payment_confirmation', booking_id=booking.id)

    # Display the booking page
    fare = 300  # Example fare calculation
    return render(request, 'book_seat.html', {'seat': seat, 'fare': fare, 'bus_id': bus_id})


@csrf_exempt
def reserve_seats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        seats_to_reserve = data.get('seats', [])
        
        for seat_number in seats_to_reserve:
            try:
                seat = Seat.objects.get(seat_number=seat_number)
                if not seat.is_reserved:
                    seat.is_reserved = True
                    seat.save()
            except Seat.DoesNotExist:
                continue

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def seat_reservation_view(request, bus_id):
    # Fetch seats for the selected bus
    seats = Seat.objects.filter(bus_id=bus_id)
    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == "POST":
        seat_number = request.POST.get("seat_number")
        if Seat.objects.filter(seat_number=seat_number, bus_id=bus_id).exists():
            messages.error(request, "Seat already exists or reserved!")
            return redirect('seat_reservation', bus_id=bus_id)

    return render(request, 'seat_reservation.html', {'seats': seats, 'bus': bus})




def success(request):
    return render(request, 'success.html')




# Create your views here.
from django.shortcuts import render
from .models import Seat, Booking

from django.shortcuts import render
from .models import Seat, Booking

def home(request):
    # Get all seats
    seats = Seat.objects.all()

    # Get the seat IDs of booked seats
    booked_seats = Booking.objects.filter(seat__isnull=False).values_list('seat__id', flat=True)

    return render(request, 'bus.html', {
        'seats': seats,
        'booked_seats': booked_seats
    })


def index(request):
    return render(request, 'index.html' )

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        doc_pat = request.POST.get("doc_pat")

        user = authenticate(request, username = username, password = password)
        if user is not None:
            authlogin(request, user)
            fname = user.first_name
            messages.success(request,' Your are successfully logged in ')
            
            return render(request, 'succcessfulllogin.html', {'fname':fname})
 
        else:
            messages.error(request, ' Username or Password did not match. Try aging.')
            return redirect('login')


    return render(request,'login.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('index')



def signUp(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        fpass = request.POST.get("pass1")
        cpass = request.POST.get("pass2")
        

        # validation for user
        if User.objects.filter(username=uname):
            messages.error(request,"Username already exist!")
            return redirect('signUp')

        if User.objects.filter(email=email):
            messages.error(request,"email already registerd")
            return redirect('signUp')

        if len(uname) >10:
            messages.error(request,"the username must be under 10 character!")
            return redirect('signUp')

        if fpass != cpass:
            messages.error(request,"Passwords didn't match.Try agian!")
            return redirect('signUp')

        if not uname.isalnum():
            messages.error(request,"Username must be alpha-numeric!")
            return redirect('signUp')

        my_user = User.objects.create_user(uname,email,fpass)
        my_user.first_name = fname
        my_user.last_name = lname

        my_user.save()

        messages.success(request, 'Thank you! your account has been successfully created.')

        return redirect('login')

    return render(request,'signUp.html')


def admin_panel(request):
    dr = Driver.objects.all().count()
    ns = NonStaff.objects.all().count()

    
    passe = Booking.objects.all()
    d = {'passe':passe, 'ns':ns, 'dr':dr}
    return render(request, 'admin.html' , d)


def passengers (request):
    passe = Booking.objects.all()
    d = {'passe':passe}
    return render(request, 'passenger.html' , d)

def bus_list (request):
    bs = Bus.objects.all().count()
    buslist = Bus.objects.all()
    d = {'bs':bs, 'buslist':buslist}
    return render(request, 'list_bus.html' , d)

#search for bus
from django.shortcuts import render
from .models import TravelSchedule, BoardingLocation, Destination

def search_buses(request):
    boarding_location = request.GET.get('boarding_location')
    destination = request.GET.get('destination')
    date_of_travel = request.GET.get('date_of_travel')
    
    buses = []
    
    if boarding_location and destination and date_of_travel:
        try:
            buses = TravelSchedule.objects.filter(
                boarding_location__name=boarding_location,
                destination__name=destination,
                date_of_travel=date_of_travel
            )
        except TravelSchedule.DoesNotExist:
            buses = []
    
    # Fetch locations and destinations for dropdowns
    boarding_locations = BoardingLocation.objects.all()
    destinations = Destination.objects.all()

    return render(request, 'new/search_results.html', {
        'buses': buses,
        'boarding_locations': boarding_locations,
        'destinations': destinations
    })


def bus_detail(request, pk):
    # Use the pk to fetch the bus schedule
    bus_schedule = get_object_or_404(TravelSchedule, pk=pk)
    
    # Fetch all seats related to the bus schedule (assuming you have a Seat model)
    seats = Seat.objects.filter(bus_schedule=bus_schedule)
    
    context = {
        'bus_schedule': bus_schedule,
        'seats': seats
    }
    
    return render(request, 'new/bus_detail.html', context)

def payment_confirmation(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        # You can add logic here to handle payment details or show a success page.
        return render(request, 'payment_confirmation.html', {'booking': booking})
    except Booking.DoesNotExist:
        # If the booking doesn't exist, show an error message
        return render(request, 'error.html', {'message': 'Booking not found.'})


# views.py
def travel_schedules_view(request):
    schedules = TravelSchedule.objects.all().select_related('bus', 'boarding_location', 'destination')
    return render(request, 'new/travel_schedules.html', {'schedules': schedules})

def schedule_bookings_view(request):
    schedule_id = request.GET.get('schedule_id')
    schedule = TravelSchedule.objects.get(id=schedule_id)
    
    # Get bookings for this specific schedule
    bookings = Booking.objects.filter(
        seat__bus_schedule=schedule
    )
    
    return render(request, 'new/schedule_bookings.html', {
        'schedule': schedule, 
        'bookings': bookings
    })

from django.shortcuts import render
from .models import TravelSchedule, Booking
from .forms import TravelScheduleSearchForm
from datetime import date

def search_travel_schedule(request):
    schedules = []
    bookings = []
    
    # Initialize date_of_travel as None
    date_of_travel = None
    
    # Check if the form is submitted with the required fields
    if request.method == 'GET':
        # Get the values from the request
        boarding_location = request.GET.get('boarding_location')
        destination = request.GET.get('destination')
        
        # Extract year, month, and day from the request and combine them into a date object
        year = request.GET.get('date_of_travel_year')
        month = request.GET.get('date_of_travel_month')
        day = request.GET.get('date_of_travel_day')
        
        if year and month and day:
            try:
                # Create the date object
                date_of_travel = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                date_of_travel = date.fromisoformat(date_of_travel)
            except ValueError:
                # If there is an error in creating the date (invalid format), set date_of_travel to None
                date_of_travel = None
        
        # If the required parameters are provided, filter schedules based on search criteria
        if boarding_location and destination and date_of_travel:
            schedules = TravelSchedule.objects.filter(
                boarding_location_id=boarding_location,
                destination_id=destination,
                date_of_travel=date_of_travel
            )

            # Fetch bookings that match the found schedules
            bookings = Booking.objects.filter(seat__bus_schedule__in=schedules)

    form = TravelScheduleSearchForm(request.GET or None)
    
    return render(request, 'new/search_travel_schedule.html', {
        'form': form,
        'schedules': schedules,
        'bookings': bookings,
    })



def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    return render(request, 'new/booking_detail.html', {
        'booking': booking
    })



def schedule_booking_details(request, schedule_id):
    # Fetch the specific schedule by its ID
    schedule = get_object_or_404(TravelSchedule, id=schedule_id)
    
    # Get all bookings related to this schedule
    bookings = Booking.objects.filter(seat__bus_schedule=schedule)
    
    return render(request, 'new/schedule_booking_details.html', {
        'schedule': schedule,
        'bookings': bookings
    })
