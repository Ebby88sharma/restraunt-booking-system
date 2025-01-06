from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),  # List all bookings for the user
    path('new/', views.create_booking, name='create_booking'),  # Create a new booking
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),  # Delete a booking
]
