from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ID', 'user', 'service_type', 'date', 'time')
    search_fields = ('user__username', 'reason', 'address')
    list_filter = ('service_type', 'date')
