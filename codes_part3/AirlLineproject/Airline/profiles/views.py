import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


logger = logging.getLogger('profiles')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"User registered and logged in: {user.email}") # ثبت لاگ
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'profiles/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User logged in: {user.email}") # ثبت لاگ
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f"User logged out: {request.user.email}") # ثبت لاگ
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        if amount:
            request.user.wallet_balance += int(amount)
            request.user.save()
            logger.info(f"User {request.user.email} charged wallet: {amount} Toman") # ثبت لاگ
            return redirect('dashboard')
    return render(request, 'profiles/dashboard.html')