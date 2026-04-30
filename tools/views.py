from django.shortcuts import render

def fertilizer_calc(request):
    return render(request, 'fertilizer_calc.html')

def profit_calc(request):
    return render(request, 'profit_calc.html')

def crop_calendar(request):
    return render(request, 'crop_calendar.html')

def market_prices(request):
    return render(request, 'market_prices.html')

def schemes(request):
    return render(request, 'schemes.html')
