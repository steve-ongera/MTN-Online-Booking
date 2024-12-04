
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
   
    path('success/', views.success, name='success'),
    
    
]
