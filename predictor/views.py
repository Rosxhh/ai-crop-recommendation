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

def _render_yield_form(request, error=None):
    """Helper to render yield_predict.html with full context."""
    context = {
        'npk_fields': [
            ('nitrogen', 'Nitrogen (N)', 'agri', '0', '140', 'fa-solid fa-seedling'),
            ('phosphorus', 'Phosphorus (P)', 'amber', '0', '145', 'fa-solid fa-cubes-stacked'),
            ('potassium', 'Potassium (K)', 'rose', '0', '205', 'fa-solid fa-flask'),
        ],
        'env_fields': [
            ('temperature', 'Temperature', '°C', 'fa-solid fa-temperature-half'),
            ('humidity', 'Relative Humidity', '%', 'fa-solid fa-droplet'),
            ('ph', 'Soil pH Level', '1-14', 'fa-solid fa-vial'),
            ('rainfall', 'Rainfall Intensity', 'mm', 'fa-solid fa-cloud-showers-heavy'),
        ],
        'error': error
    }
    return render(request, "yield_predict.html", context)


def predict_yield(request):
    if request.method == "POST":
        try:
            # 🔒 SECURITY: Sanitize and validate 'area' input
            try:
                area = float(request.POST.get("area") or 0)
            except (ValueError, TypeError):
                return _render_yield_form(request, "Invalid area value. Please enter a number.")

            # Clamp area to a realistic agricultural range (0.01 – 100,000 hectares)
            area = _clamp(area, 0.01, 100_000)

            # 🔒 SECURITY: Whitelist-validate the region input
            region = request.POST.get("region", "").strip().lower()
            if region not in VALID_REGIONS:
                return _render_yield_form(request, "Invalid region selected. Please choose a valid region.")

            r_data = REGION_DATA.get(region, {})

            # Get manual inputs if provided, else fallback to region defaults
            try:
                nitrogen = float(request.POST.get("nitrogen") or r_data.get("N", 90))
                phosphorus = float(request.POST.get("phosphorus") or r_data.get("P", 42))
                potassium = float(request.POST.get("potassium") or r_data.get("K", 43))
                temperature = float(request.POST.get("temperature") or r_data.get("temperature", 28.5))
                humidity = float(request.POST.get("humidity") or r_data.get("humidity", 80))
                ph = float(request.POST.get("ph") or r_data.get("ph", 6.5))
                rainfall = float(request.POST.get("rainfall") or r_data.get("rainfall", 120.5))
            except ValueError:
                return _render_yield_form(request, "Invalid numeric input for soil/weather data.")

            # Model input: X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Area']]
            import pandas as pd
            feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Area']
            input_df = pd.DataFrame([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, area]], columns=feature_names)

            prediction = model.predict(input_df)
            total_yield = round(float(prediction[0]), 2)  # type: ignore
            yield_per_hectare = round(float(total_yield / area), 2) if area > 0 else 0.0  # type: ignore

            crop_name = request.POST.get("crop", "Unknown")
            soil_name = request.POST.get("soil", "Unknown")

            # 1. Advanced Feature: Revenue Estimation
            crop_prices = {
                "wheat": 22000,
                "rice": 25000,
                "maize": 18000,
                "cotton": 65000,
                "sugarcane": 3000,
                "soybean": 45000
            }
            price_per_ton = crop_prices.get(crop_name.lower(), 15000)
            revenue = round(total_yield * price_per_ton)

            # 2. Advanced Feature: Suitability Score
            n_score = min(100, (nitrogen / 120) * 100) if nitrogen < 120 else 100 - (nitrogen-120)
            p_score = min(100, (phosphorus / 60) * 100) if phosphorus < 60 else 100 - (phosphorus-60)
            k_score = min(100, (potassium / 60) * 100) if potassium < 60 else 100 - (potassium-60)
            suitability = max(40, round((n_score + p_score + k_score) / 3)) # Ensure minimum 40%

            # 3. Advanced Feature: Actionable Insights
            tips = []
            if nitrogen < 80:
                tips.append(f"Apply nitrogen-rich fertilizers to boost {crop_name.title()}'s vegetative growth.")
            else:
                tips.append("Nitrogen levels are optimal. Avoid over-fertilizing to prevent lodging.")
                
            if rainfall < 100:
                tips.append(f"Low rainfall ({rainfall}mm). Ensure adequate irrigation systems are active.")
            else:
                tips.append(f"Rainfall ({rainfall}mm) is adequate. Monitor for waterlogging if soil drainage is poor.")
                
            if ph < 6.0:
                tips.append(f"Soil pH is acidic ({ph}). Consider applying agricultural lime to balance it.")
            elif ph > 7.5:
                tips.append(f"Soil pH is alkaline ({ph}). Use organic compost to improve soil acidity.")
            else:
                tips.append(f"{soil_name.title()} soil has ideal pH ({ph}) for maximum nutrient absorption.")

            # Pass all data to result.html for visualization
            context = {
                "yield": total_yield,
                "yield_ph": yield_per_hectare,
                "revenue": revenue,
                "suitability": suitability,
                "tips": tips,
                "inputs": {
                    "crop": crop_name,
                    "soil": soil_name,
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

            return render(request, "yield_result.html", context)

        except Exception as e:
            return _render_yield_form(request, f"Analysis failed: {str(e)}")

    return _render_yield_form(request)