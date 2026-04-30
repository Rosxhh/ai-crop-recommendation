import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import LoginHistory
from django.utils import timezone


API_KEY = "946a968623cdfce53a6c3cc031c29580"


# Dashboard (Home) - Protected
@login_required(login_url='/')
def home(request):
    return render(request, "home.html")


def _record_login(request, user):
    """Helper to record login event"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    device = "Mobile" if "Mobile" in user_agent else "Desktop"
    
    LoginHistory.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent,
        device_type=device
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        identity = request.POST.get("email") # The form field is still named 'email'
        password = request.POST.get("password")
        
        try:
            # Try finding user by email or username
            user_obj = User.objects.filter(email=identity).first() or User.objects.filter(username=identity).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    _record_login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Invalid password credentials.")
            else:
                messages.error(request, "No account associated with this email or username.")
        except Exception as e:
            messages.error(request, "An error occurred during login.")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Account with this email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
        else:
            # If username is empty, derive from email
            if not username:
                username = email.split('@')[0]
                original_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()
            
            # Auto login after register
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            _record_login(request, user)
            return redirect('home')
            
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


# Satellite Farm Map
@login_required(login_url='/')
def satellite_map(request):
    return render(request, "satellite_map.html")


# Weather Page
@login_required(login_url='/')
def weather_view(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "rainfall": data.get("rain", {}).get("1h", 0)
        }
        return JsonResponse(weather)

    return render(request, "weather.html")

@login_required(login_url='/')
def login_history_view(request):
    history = LoginHistory.objects.filter(user=request.user)[:20]
    return render(request, "login_history.html", {"history": history})