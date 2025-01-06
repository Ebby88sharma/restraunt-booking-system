from django.db import models
from users.models import CustomUser

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.IntegerField()
    
    class Meta:
        unique_together = ('table', 'booking_date', 'booking_time')

    def __str__(self):
        return f"{self.user.username} booked Table {self.table.table_number} on {self.booking_date} at {self.booking_time}"