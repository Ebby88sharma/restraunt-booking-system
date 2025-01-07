from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Table, Booking
from django.http import JsonResponse
from django.contrib import messages


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
            messages.error(request, 'All fields are required!')
        else:
            # Check if the table exists
            try:
                table = Table.objects.get(id=table_id)
            except Table.DoesNotExist:
                messages.error(request, 'Invalid table selection!')
            else:
                # Create the booking
                Booking.objects.create(
                    user=request.user,
                    table=table,
                    booking_date=booking_date,
                    booking_time=booking_time,
                    guests=guests
                )
                messages.success(request, 'Booking created successfully!')
                return redirect('booking_list')  # Redirect to My Bookings page

    # GET request: Show the booking creation form
    tables = Table.objects.all()
    return render(request, 'bookings/create_booking.html', {'tables': tables})


@login_required
def booking_list(request):
    """View to list all bookings for the logged-in user."""
    bookings = Booking.objects.filter(user=request.user)  # Fetch bookings for the logged-in user
    messages.info(request, 'Here are your current bookings.')  # Example informational message
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def dashboard(request):
    """View for the dashboard displaying booking statistics."""
    total_tables = Table.objects.count()
    total_bookings = Booking.objects.count()
    user_bookings = Booking.objects.filter(user=request.user).count()
    messages.success(request, 'Welcome to your dashboard!')  # Dashboard welcome message
    return render(request, 'bookings/dashboard.html', {
        'total_tables': total_tables,
        'total_bookings': total_bookings,
        'user_bookings': user_bookings,
    })


@login_required
def delete_booking(request, booking_id):
    """View to delete a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Check if booking exists for the user
    if request.method == 'POST':  # Ensure it's a POST request
        booking.delete()  # Delete the booking
        messages.success(request, 'Booking deleted successfully!')
        return redirect('booking_list')  # Redirect to the booking list
    messages.warning(request, 'Are you sure you want to delete this booking?')  # Confirmation warning
    return render(request, 'bookings/confirm_delete.html', {'booking': booking})
