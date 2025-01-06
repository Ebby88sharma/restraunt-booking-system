from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Table, Booking
from django.http import JsonResponse


@login_required
def booking_list(request):
    """View to list all bookings for the logged-in user."""
    bookings = Booking.objects.filter(user=request.user)  # Fetch bookings for the logged-in user
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    """View to delete a booking."""
    if request.method == 'DELETE':  # Ensure it's a DELETE request
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Check if booking exists
        booking.delete()  # Delete the booking
        return JsonResponse({'message': 'Booking deleted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def create_booking(request):
    """View to handle booking creation."""
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        guests = request.POST.get('guests')

        # Validate data
        if not all([table_id, booking_date, booking_time, guests]):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        # Check if the table exists
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return JsonResponse({'error': 'Invalid table selection!'}, status=404)

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            table=table,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests
        )
        return JsonResponse({'message': 'Booking created successfully!'}, status=201)

    # GET request: Show the booking creation form
    tables = Table.objects.all()
    return render(request, 'bookings/create_booking.html', {'tables': tables})
