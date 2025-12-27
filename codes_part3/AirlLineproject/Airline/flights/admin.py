from django.contrib import admin
from .models import Airport, Airline, Route, Flight, Reservation

from django.contrib.sessions.models import Session


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    list_display = [
        'airline',
        'route',
        'departure_time',
        'total_seats',
        'available_seats',
        'get_sold_count',
        'airplane_type'
    ]


    list_filter = ['airline', 'departure_time']


    def get_sold_count(self, obj):
        sold = obj.total_seats - obj.available_seats
        return f"{sold} عدد"

    get_sold_count.short_description = "بلیط‌های فروخته شده"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ['user', 'flight', 'purchased_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']

    search_fields = ['user__email', 'flight__route__origin__name']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']



admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Route)