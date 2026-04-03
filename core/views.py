import requests
from django.shortcuts import render
from django.http import JsonResponse


API_KEY = "946a968623cdfce53a6c3cc031c29580"


# Home Page
def home(request):
    return render(request, "home.html")


# Satellite Farm Map
def satellite_map(request):
    return render(request, "satellite_map.html")


# Weather Page
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