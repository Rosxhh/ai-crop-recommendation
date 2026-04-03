import os
import joblib
import numpy as np
from django.shortcuts import render
from django.conf import settings


# -------------------------------------------------------
# 🔒 SECURITY: Input validation helper
# -------------------------------------------------------
def _safe_float(value, default=0.0, min_val=None, max_val=None):
    """Parse a float safely and optionally clamp to [min_val, max_val]."""
    try:
        result = float(value or default)
    except (ValueError, TypeError):
        result = default
    if min_val is not None:
        result = max(min_val, result)
    if max_val is not None:
        result = min(max_val, result)
    return result


# --------------------------------------------------
# LOAD MODEL (runs once when server starts)
# --------------------------------------------------
model_path = os.path.join(settings.BASE_DIR, "crop1.pkl")

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print("Recommendation model file not found!")


# --------------------------------------------------
# VIEW FUNCTION
# --------------------------------------------------
def recommend_crop(request):

    if request.method == "POST":

        if model is None:
            return render(request, "recommend.html", {
                "error": "Model file not found!"
            })

        try:
            # 🔒 SECURITY: Sanitize all inputs with type-safe parsing + range clamping
            # Valid agronomic ranges based on standard soil/climate datasets
            nitrogen    = _safe_float(request.POST.get("nitrogen"),    0, 0, 300)   # kg/ha
            phosphorus  = _safe_float(request.POST.get("phosphorus"),  0, 0, 300)   # kg/ha
            potassium   = _safe_float(request.POST.get("potassium"),   0, 0, 300)   # kg/ha
            temperature = _safe_float(request.POST.get("temperature"), 0, -10, 60)  # °C
            humidity    = _safe_float(request.POST.get("humidity"),    0, 0, 100)   # %
            ph          = _safe_float(request.POST.get("ph"),          0, 0, 14)    # pH scale
            rainfall    = _safe_float(request.POST.get("rainfall"),    0, 0, 5000)  # mm/year

            # Create input array
            input_data = np.array([[
                nitrogen,
                phosphorus,
                potassium,
                temperature,
                humidity,
                ph,
                rainfall
            ]])

            # Predict
            prediction = model.predict(input_data)
            from .crop_info import get_crop_data
            crop_data = get_crop_data(int(prediction[0]))

            return render(request, "result.html", {
                "crop": crop_data['name'],
                "crop_details": crop_data
            })

        except ValueError:
            return render(request, "recommend.html", {
                "error": "Please enter valid numeric values!"
            })

        except Exception as e:
            return render(request, "recommend.html", {
                "error": f"Unexpected error: {str(e)}"
            })

    return render(request, "recommend.html")