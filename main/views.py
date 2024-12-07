
from django.shortcuts import render, redirect 
from .models import Destination, BoardingLocation , Seat
from .forms import *
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
from django.shortcuts import get_object_or_404
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

    # Fetch the TravelSchedule and related details
    travel_schedule = get_object_or_404(TravelSchedule, bus_id=bus_id)
    fare = travel_schedule.fare
    bus_name = travel_schedule.bus.name
    boarding_location = travel_schedule.boarding_location.name
    destination = travel_schedule.destination.name
    date_of_travel = travel_schedule.date_of_travel
    departure_time = travel_schedule.departure_time

    # If the user submits the booking form
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        identification_number = request.POST.get('identification_number')

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
    context = {
        'seat': seat,
        'fare': fare,
        'bus_name': bus_name,
        'boarding_location': boarding_location,
        'destination': destination,
        'date_of_travel': date_of_travel,
        'departure_time': departure_time,
        'bus_id': bus_id,
    }
    return render(request, 'book_seat.html', context)



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

    # Add available seats calculation to each bus schedule
    for bus in buses:
        total_seats = Seat.objects.filter(bus_schedule=bus).count()
        reserved_seats = Seat.objects.filter(bus_schedule=bus, is_reserved=True).count()
        bus.available_seats = total_seats - reserved_seats  # Add available seats as an attribute

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
    # Get available seat numbers
    available_seats = seats.filter(is_reserved=False).values_list('seat_number', flat=True)
    

    
    context = {
        'bus_schedule': bus_schedule,
        'seats': seats,
        'available_seats': available_seats,  # Pass available seat numbers to the template
    }
    
    return render(request, 'new/bus_detail.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Booking
from .utils import generate_professional_ticket_pdf, send_professional_ticket_email

def payment_confirmation(request, booking_id):
    try:
        # Get the booking object
        booking = Booking.objects.get(id=booking_id)

        # Generate the PDF receipt
        pdf_buffer = generate_professional_ticket_pdf(booking)

        # Send the receipt as an email attachment
        send_professional_ticket_email(booking, pdf_buffer)

        # Render the payment confirmation page
        return render(request, 'payment_confirmation.html', {'booking': booking})

    except Booking.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found.'})


# views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from .models import Booking

def download_receipt(request, booking_id):
    # Get the booking object based on the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Create the response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.id}.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response, pagesize=letter)

    # Header (Company Information)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 770, "Your Company Name")
    p.setFont("Helvetica", 10)
    p.drawString(200, 755, "Address: 123 Main Street, City, Country")
    p.drawString(200, 740, "Phone: +1234567890")
    p.drawString(200, 725, "Email: support@yourcompany.com")

    # Receipt Title
    p.setFont("Helvetica-Bold", 12)
    p.drawString(200, 700, "Receipt")

    # Booking Details Section
    p.setFont("Helvetica", 10)
    p.drawString(50, 675, f"Booking ID: {booking.id}")
    p.drawString(50, 660, f"Name: {booking.name}")
    p.drawString(50, 645, f"Email: {booking.email}")
    p.drawString(50, 630, f"Phone: {booking.phone}")
    p.drawString(50, 615, f"Seat Number: {booking.seat.seat_number if booking.seat else 'No seat assigned'}")
    p.drawString(50, 600, f"Identification Number: {booking.identification_number}")

    # Fare Section
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, 570, f"Total Fare: ${booking.fare}")

    # Footer
    p.setFont("Helvetica", 8)
    p.drawString(50, 50, "Thank you for booking with us!")
    p.drawString(50, 40, "Visit us again for more exciting offers.")

    # Draw a line to separate footer
    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    p.line(50, 60, 550, 60)

    # Save the PDF
    p.showPage()
    p.save()

    return response



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

#travel schedule views 

def travel_schedule_create(request):
    if request.method == 'POST':
        form = TravelScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('travel_schedule_list')  # Redirect to the list after creating
    else:
        form = TravelScheduleForm()
    return render(request, 'travel_schedule/travel_schedule_form.html', {'form': form})


def travel_schedule_list(request):
    schedules = TravelSchedule.objects.all()
    return render(request, 'travel_schedule/travel_schedule_list.html', {'schedules': schedules})



def travel_schedule_update(request, schedule_id):
    schedule = get_object_or_404(TravelSchedule, id=schedule_id)
    
    if request.method == 'POST':
        form = TravelScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('travel_schedule_list')  # Redirect to the list after updating
    else:
        form = TravelScheduleForm(instance=schedule)
    
    return render(request, 'travel_schedule/travel_schedule_form.html', {'form': form, 'schedule': schedule})



def travel_schedule_delete(request, schedule_id):
    schedule = get_object_or_404(TravelSchedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        return redirect('travel_schedule_list')  # Redirect to the list after deletion
    return render(request, 'travel_schedule/travel_schedule_confirm_delete.html', {'schedule': schedule})


#Bus views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Bus
from .forms import BusForm

# Create View
def bus_create(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bus_list')  # Redirect to the bus list after creating
    else:
        form = BusForm()
    return render(request, 'bus/bus_form.html', {'form': form})

# List View
def bus_list(request):
    buses = Bus.objects.all()
    return render(request, 'bus/bus_list.html', {'buses': buses})

# Update View
def bus_update(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect('bus_list')  # Redirect to the bus list after updating
    else:
        form = BusForm(instance=bus)
    
    return render(request, 'bus/bus_form.html', {'form': form, 'bus': bus})

# Delete View
def bus_delete(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    if request.method == 'POST':
        bus.delete()
        return redirect('bus_list')  # Redirect to the bus list after deletion
    return render(request, 'bus/bus_confirm_delete.html', {'bus': bus})


#drivers views


# Create View
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')  # Redirect to the driver list after creating
    else:
        form = DriverForm()
    return render(request, 'driver/driver_form.html', {'form': form})

# List View
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'driver/driver_list.html', {'drivers': drivers})

# Update View
def driver_update(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')  # Redirect to the driver list after updating
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'driver/driver_form.html', {'form': form, 'driver': driver})

# Delete View
def driver_delete(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')  # Redirect to the driver list after deletion
    return render(request, 'driver/driver_confirm_delete.html', {'driver': driver})


#destination 
# Create View
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination_list')  # Redirect to the destination list after creating
    else:
        form = DestinationForm()
    return render(request, 'destination/destination_form.html', {'form': form})

# List View
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination/destination_list.html', {'destinations': destinations})

# Update View
def destination_update(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_list')  # Redirect to the destination list after updating
    else:
        form = DestinationForm(instance=destination)
    
    return render(request, 'destination/destination_form.html', {'form': form, 'destination': destination})

# Delete View
def destination_delete(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        destination.delete()
        return redirect('destination_list')  # Redirect to the destination list after deletion
    return render(request, 'destination/destination_confirm_delete.html', {'destination': destination})



#boarding

# Create View
def boarding_location_create(request):
    if request.method == 'POST':
        form = BoardingLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boarding_location_list')  # Redirect to the list of boarding locations
    else:
        form = BoardingLocationForm()
    return render(request, 'boarding_location/boarding_location_form.html', {'form': form})

# List View
def boarding_location_list(request):
    boarding_locations = BoardingLocation.objects.all()
    return render(request, 'boarding_location/boarding_location_list.html', {'boarding_locations': boarding_locations})

# Update View
def boarding_location_update(request, location_id):
    location = get_object_or_404(BoardingLocation, id=location_id)
    
    if request.method == 'POST':
        form = BoardingLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('boarding_location_list')  # Redirect after update
    else:
        form = BoardingLocationForm(instance=location)
    
    return render(request, 'boarding_location/boarding_location_form.html', {'form': form, 'location': location})

# Delete View
def boarding_location_delete(request, location_id):
    location = get_object_or_404(BoardingLocation, id=location_id)
    if request.method == 'POST':
        location.delete()
        return redirect('boarding_location_list')  # Redirect after deletion
    return render(request, 'boarding_location/boarding_location_confirm_delete.html', {'location': location})


#booking views

# Create View
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_list')  # Redirect to the list of bookings
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})

# List View
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# Update View
def booking_update(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')  # Redirect after update
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'booking/booking_form.html', {'form': form, 'booking': booking})

# Delete View
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')  # Redirect after deletion
    return render(request, 'booking/booking_confirm_delete.html', {'booking': booking})


#non staff views

# Create View
def non_staff_create(request):
    if request.method == 'POST':
        form = NonStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('non_staff_list')  # Redirect to the list view
    else:
        form = NonStaffForm()
    return render(request, 'non_staff/non_staff_form.html', {'form': form})

# List View
def non_staff_list(request):
    non_staffs = NonStaff.objects.all()
    return render(request, 'non_staff/non_staff_list.html', {'non_staffs': non_staffs})

# Update View
def non_staff_update(request, non_staff_id):
    non_staff = get_object_or_404(NonStaff, id=non_staff_id)
    
    if request.method == 'POST':
        form = NonStaffForm(request.POST, instance=non_staff)
        if form.is_valid():
            form.save()
            return redirect('non_staff_list')  # Redirect after update
    else:
        form = NonStaffForm(instance=non_staff)
    
    return render(request, 'non_staff/non_staff_form.html', {'form': form, 'non_staff': non_staff})

# Delete View
def non_staff_delete(request, non_staff_id):
    non_staff = get_object_or_404(NonStaff, id=non_staff_id)
    if request.method == 'POST':
        non_staff.delete()
        return redirect('non_staff_list')  # Redirect after deletion
    return render(request, 'non_staff/non_staff_confirm_delete.html', {'non_staff': non_staff})
