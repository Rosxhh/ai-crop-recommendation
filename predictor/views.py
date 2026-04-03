import os
import joblib  # type: ignore
import numpy as np  # type: ignore
from django.shortcuts import render  # type: ignore
from django.conf import settings  # type: ignore
from .models import YieldPrediction

# Load Model
model_path = os.path.join(settings.BASE_DIR, "yield_model.pkl")
model = joblib.load(model_path)

REGION_DATA = {
    "north": {"N": 100, "P": 50, "K": 40, "temperature": 25.0, "humidity": 60.0, "ph": 7.0, "rainfall": 80.0},
    "south": {"N": 80, "P": 40, "K": 50, "temperature": 30.0, "humidity": 85.0, "ph": 6.8, "rainfall": 200.0},
    "east": {"N": 85, "P": 45, "K": 40, "temperature": 28.0, "humidity": 80.0, "ph": 6.2, "rainfall": 180.0},
    "west": {"N": 70, "P": 50, "K": 45, "temperature": 32.0, "humidity": 55.0, "ph": 6.8, "rainfall": 70.0},
    "central": {"N": 90, "P": 45, "K": 40, "temperature": 29.0, "humidity": 65.0, "ph": 7.2, "rainfall": 100.0},
}

# -------------------------------------------------------
# 🔒 SECURITY: Input validation helper
# -------------------------------------------------------
VALID_REGIONS = set(REGION_DATA.keys())  # whitelist of accepted region values

def _clamp(value, min_val, max_val):
    """Clamp a numeric value to [min_val, max_val]."""
    return max(min_val, min(max_val, value))


def predict_yield(request):
    if request.method == "POST":
        try:
            # 🔒 SECURITY: Sanitize and validate 'area' input
            try:
                area = float(request.POST.get("area") or 0)
            except (ValueError, TypeError):
                return render(request, "index.html", {"error": "Invalid area value. Please enter a number."})

            # Clamp area to a realistic agricultural range (0.01 – 100,000 hectares)
            area = _clamp(area, 0.01, 100_000)

            # 🔒 SECURITY: Whitelist-validate the region input
            region = request.POST.get("region", "").strip().lower()
            if region not in VALID_REGIONS:
                return render(request, "index.html", {"error": "Invalid region selected. Please choose a valid region."})

            
            if region in REGION_DATA:
                r_data = REGION_DATA[region]
                nitrogen = r_data["N"]
                phosphorus = r_data["P"]
                potassium = r_data["K"]
                temperature = r_data["temperature"]
                humidity = r_data["humidity"]
                ph = r_data["ph"]
                rainfall = r_data["rainfall"]
            else:
                # Default fallback
                nitrogen = 90
                phosphorus = 42
                potassium = 43
                temperature = 28.5
                humidity = 80
                ph = 6.5
                rainfall = 120.5

            # Model input: X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Area']]
            # Order must match training: N, P, K, temp, humidity, ph, rain, area
            input_data = np.array([[
                nitrogen, 
                phosphorus, 
                potassium, 
                temperature, 
                humidity, 
                ph, 
                rainfall, 
                area
            ]])

            prediction = model.predict(input_data)
            total_yield = round(float(prediction[0]), 2)  # type: ignore
            yield_per_hectare = round(float(total_yield / area), 2) if area > 0 else 0.0  # type: ignore

            # SAVE TO DATABASE (Updating model if necessary, for now use existing fields or placeholders)
            # YieldPrediction.objects.create(...)
            
            # Pass all data to result.html for visualization
            context = {
                "yield": total_yield,
                "yield_ph": yield_per_hectare,
                "inputs": {
                    "nitrogen": nitrogen,
                    "phosphorus": phosphorus,
                    "potassium": potassium,
                    "temperature": temperature,
                    "humidity": humidity,
                    "ph": ph,
                    "rainfall": rainfall,
                    "area": area
                }
            }

            return render(request, "result.html", context)

        except Exception as e:
            return render(request, "index.html", {
                "error": f"Numeric analysis failed: {str(e)}"
            })

    return render(request, "index.html")