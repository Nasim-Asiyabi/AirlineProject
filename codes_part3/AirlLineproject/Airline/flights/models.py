from django.db import models
from django.conf import settings

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    def __str__(self): return f"{self.name} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Route(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    def __str__(self): return f"{self.origin} to {self.destination}"

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    price = models.BigIntegerField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    airplane_type = models.CharField(max_length=50, default="Boeing 737")
    cancellation_fee_percent = models.FloatField(default=0.20)

    def __str__(self): return f"{self.airline.name} - {self.route}"

class Reservation(models.Model):
    STATUS_CHOICES = [('PUR', 'Purchased'), ('CAN', 'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    purchased_price = models.BigIntegerField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PUR')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.user} - {self.flight}"