from django.contrib import admin
from .models import Court, Booking

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_hour')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'court', 'booking_date', 'start_time', 'duration', 'status', 'total_price')
    list_filter = ('status', 'booking_date', 'court')
    search_fields = ('customer_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    ordering = ('-booking_date', '-start_time')
