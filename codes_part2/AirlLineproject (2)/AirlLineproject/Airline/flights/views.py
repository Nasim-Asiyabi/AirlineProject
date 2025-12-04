from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flight, Reservation


def home_view(request):
    flights = Flight.objects.all()
    if request.GET.get('origin'):
        flights = flights.filter(route__origin__name__icontains=request.GET['origin'])
    if request.GET.get('destination'):
        flights = flights.filter(route__destination__name__icontains=request.GET['destination'])
    return render(request, 'flights/home.html', {'flights': flights})


@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.user.wallet_balance >= flight.price and flight.available_seats > 0:
        request.user.wallet_balance -= flight.price
        request.user.save()

        flight.available_seats -= 1
        flight.save()

        Reservation.objects.create(user=request.user, flight=flight, purchased_price=flight.price)

    return redirect('dashboard')


@login_required
def cancel_flight(request, reservation_id):
    res = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if res.status == 'PUR':
        # تغییر مهم: چون قیمت عدد صحیح و درصد اعشار است، نتیجه را int میکنیم
        penalty = int(res.purchased_price * res.flight.cancellation_fee_percent)
        refund_amount = res.purchased_price - penalty

        request.user.wallet_balance += refund_amount
        request.user.save()

        res.status = 'CAN'
        res.save()

        res.flight.available_seats += 1
        res.flight.save()

    return redirect('dashboard')