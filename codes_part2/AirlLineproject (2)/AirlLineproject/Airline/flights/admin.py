from django.contrib import admin
from .models import Airport, Airline, Route, Flight, Reservation

admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Reservation)