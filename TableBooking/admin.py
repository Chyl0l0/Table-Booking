from django.contrib import admin
from TableBooking.models import Room, Table, Booking
# Register your models here.

admin.site.register(Room)
admin.site.register(Table)
admin.site.register(Booking)
