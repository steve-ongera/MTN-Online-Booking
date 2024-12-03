
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

@csrf_exempt
def confirm_booking(request):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        fare = request.POST.get('fare')
        identification_number = request.POST.get('identification_number')

        try:
            seat = Seat.objects.get(seat_number=seat_number)
            if seat.is_reserved:
                messages.error(request, ' Book Tena Ishachukuliwa')
                return redirect('seat_reservation')  # Redirect if seat is already reserved

            # Save the booking
            Booking.objects.create(seat=seat, name=name, email=email, phone=phone, fare=fare , identification_number=identification_number)

            # Mark the seat as reserved
            seat.is_reserved = True
            seat.save()
            messages.success(request, 'Succesfuly Booking . You will receive Ticket in your email')
            return redirect('success')  # Redirect to the seat reservation page after booking

        except Seat.DoesNotExist:
            return redirect('seat_reservation')  # Redirect if seat does not exist

    return redirect('seat_reservation')




def book_seats(request):
    
    seat_number = request.GET.get('seat')
    if not seat_number:
        return redirect('seat_reservation')  # Redirect if no seat is selected

    try:
        seat = Seat.objects.get(seat_number=seat_number)
        if seat.is_reserved:
            messages.success(request, 'The seat you selected is already Booked!')
            return redirect('seat_reservation' )  # Redirect if seat is already reserved
    except Seat.DoesNotExist:
        return redirect('seat_reservation')  # Redirect if seat does not exist

    fare = 300  # Example fare calculation
    return render(request, 'book_seat.html', {'seat': seat, 'fare': fare})

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


def seat_reservation_view(request):
    seats = Seat.objects.all()
    if request.method == "POST":
        seat_number = request.POST.get("seat_number")
        
        if Seat.objects.filter(seat_number=seat_number):
                messages.error(request,"seat already exist!")
                return redirect('seat_reservation')
     
    
    return render(request, 'seat_reservation.html', {'seats': seats})




def success(request):
    return render(request, 'success.html')




# Create your views here.
def home(request):
    seats = Seat.objects.all()
    return render(request, 'bus.html' , {'seats': seats})


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



