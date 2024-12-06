
from django.urls import path
from . import views

urlpatterns = [
    path('online_booking', views.home , name='home'),
    path('bus_list', views.bus_list , name='bus_list'),
    path('admi_panel', views.admin_panel, name='admin_panel'),
    #path('book/', views.book_seats, name='book_seats'),
    path('success/', views.success, name='success'),
    path('', views.index, name='index'),
    path('passengers', views.passengers , name='passengers'),
    path('signUp',views.signUp,name = 'signUp'),
    path('login',views.login,name = 'login'),
    path('signout',views.signout,name = 'signout'),
    #path('reserve/', views.seat_reservation_view, name='seat_reservation'),
    path('reserve_seats/', views.reserve_seats, name='reserve_seats'),
    #path('book_seats/', views.book_seats, name='book_seats'),
    #path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    #new urls
    path('search-buses/', views.search_buses, name='search_buses'),
    path('bus/<int:pk>/', views.bus_detail, name='bus_detail'),

    path('seat_reservation/<int:bus_id>/', views.seat_reservation_view, name='seat_reservation'),
    path('book_seats/<int:bus_id>/', views.book_seats, name='book_seats'),
    path('confirm_booking/<int:bus_id>/', views.confirm_booking, name='confirm_booking'),
    path('payment/confirmation/<int:booking_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('download_receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),
   
    path('success/', views.success, name='success'),

    path('travel-schedules/', views.travel_schedules_view, name='travel_schedules'),
    path('schedule-bookings/', views.schedule_bookings_view, name='schedule_bookings'),
    path('search_schedule/', views.search_travel_schedule, name='search_travel_schedule'),
    path('booking_detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('schedule_booking_details/<int:schedule_id>/', views.schedule_booking_details, name='schedule_booking_details'),
    #travel schedule 
    path('travel_schedule/', views.travel_schedule_list, name='travel_schedule_list'),  # List
    path('travel_schedule/create/', views.travel_schedule_create, name='travel_schedule_create'),  # Create
    path('travel_schedule/<int:schedule_id>/update/', views.travel_schedule_update, name='travel_schedule_update'),  # Update
    path('travel_schedule/<int:schedule_id>/delete/', views.travel_schedule_delete, name='travel_schedule_delete'),  # Delete
    #bus views
    path('bus/', views.bus_list, name='bus_list'),  # List view
    path('bus/create/', views.bus_create, name='bus_create'),  # Create view
    path('bus/<int:bus_id>/update/', views.bus_update, name='bus_update'),  # Update view
    path('bus/<int:bus_id>/delete/', views.bus_delete, name='bus_delete'),  # Delete view
    #drivers
    path('driver/', views.driver_list, name='driver_list'),  # List view
    path('driver/create/', views.driver_create, name='driver_create'),  # Create view
    path('driver/<int:driver_id>/update/', views.driver_update, name='driver_update'),  # Update view
    path('driver/<int:driver_id>/delete/', views.driver_delete, name='driver_delete'),  # Delete view
    #destination
    path('destination/', views.destination_list, name='destination_list'),  # List view
    path('destination/create/', views.destination_create, name='destination_create'),  # Create view
    path('destination/<int:destination_id>/update/', views.destination_update, name='destination_update'),  # Update view
    path('destination/<int:destination_id>/delete/', views.destination_delete, name='destination_delete'),  # Delete view
    #boarding
    path('boarding_location/', views.boarding_location_list, name='boarding_location_list'),  # List view
    path('boarding_location/create/', views.boarding_location_create, name='boarding_location_create'),  # Create view
    path('boarding_location/<int:location_id>/update/', views.boarding_location_update, name='boarding_location_update'),  # Update view
    path('boarding_location/<int:location_id>/delete/', views.boarding_location_delete, name='boarding_location_delete'),  # Delete view
    #booking
    path('booking/', views.booking_list, name='booking_list'),  # List view
    path('booking/create/', views.booking_create, name='booking_create'),  # Create view
    path('booking/<int:booking_id>/update/', views.booking_update, name='booking_update'),  # Update view
    path('booking/<int:booking_id>/delete/', views.booking_delete, name='booking_delete'),  # Delete view
    #non staff
    path('non_staff/', views.non_staff_list, name='non_staff_list'),  # List view
    path('non_staff/create/', views.non_staff_create, name='non_staff_create'),  # Create view
    path('non_staff/<int:non_staff_id>/update/', views.non_staff_update, name='non_staff_update'),  # Update view
    path('non_staff/<int:non_staff_id>/delete/', views.non_staff_delete, name='non_staff_delete'),  # Delete view
  
]
