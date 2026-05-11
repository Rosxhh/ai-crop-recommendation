import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import LoginHistory, UserProfile
from django.utils import timezone
from django.db import IntegrityError

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
    # Support for Guest Mode
    if request.GET.get('mode') == 'guest':
        guest_user, created = User.objects.get_or_create(username='guest_explorer', email='guest@agricore.ai')
        if created:
            guest_user.set_unusable_password()
            guest_user.save()
            UserProfile.objects.get_or_create(user=guest_user)
        
        login(request, guest_user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, "You are now exploring as a Guest. Welcome!")
        return redirect('home')

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        identity = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            # Try finding user by email, mobile, or username
            user_obj = User.objects.filter(email=identity).first() or \
                       User.objects.filter(username=identity).first() or \
                       User.objects.filter(profile__mobile=identity).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    _record_login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                    return redirect('home')
                else:
                    messages.error(request, "We couldn't sign you in. Please check your password and try again.")
            else:
                messages.error(request, "We couldn't find an account associated with that information.")
        except Exception:
            messages.error(request, "A technical issue occurred. Please try again in a few moments.")

    try:
        return render(request, "login.html")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Login Template Rendering Error: {e}")
        from django.http import HttpResponse
        return HttpResponse(f"AgriCore Service is initializing. Please refresh in 30 seconds. (Diagnostic: {str(e)})", status=200)

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists. Please try signing in.")
        elif UserProfile.objects.filter(mobile=mobile).exists():
            messages.error(request, "This mobile number is already registered with another account.")
        else:
            try:
                # Generate unique username from email
                username = email.split('@')[0]
                original_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                    
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = name
                user.save()
                
                # Create profile with mobile (handle empty as None)
                UserProfile.objects.create(user=user, mobile=mobile if mobile else None)
                
                # Auto login after register
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                _record_login(request, user)
                messages.success(request, "Account created successfully! Welcome to AgriCore.")
                return redirect('home')
            except IntegrityError as ie:
                messages.error(request, f"Registration conflict: {str(ie)}. Please check if your email/mobile is already used.")
            except Exception as e:
                messages.error(request, f"Technical issue: {str(e)}")
            
    try:
        return render(request, "register.html")
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f"AgriCore Service (Reg) is initializing. Please refresh. (Diag: {str(e)})", status=200)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been securely signed out.")
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

def health_check(request):
    return JsonResponse({"status": "AgriCore Online", "timestamp": timezone.now()})