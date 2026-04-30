import os
import joblib
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings
from .models import CropRecommendation


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
# VIEW FUNCTIONS
# --------------------------------------------------
def recommend_crop(request):
    
    # Metadata for professional field rendering
    context_data = {
        "npk_fields": [
            ("nitrogen", "Nitrogen (N)", "emerald", 0, 140, "fa-solid fa-vial"),
            ("phosphorus", "Phosphorus (P)", "blue", 0, 145, "fa-solid fa-flask-vial"),
            ("potassium", "Potassium (K)", "amber", 0, 205, "fa-solid fa-vial-circle-check"),
        ],
        "env_fields": [
            ("temperature", "Temperature", "°C", "fa-solid fa-temperature-three-quarters"),
            ("humidity", "Relative Humidity", "%", "fa-solid fa-droplet"),
            ("ph", "Soil pH Level", "1-14", "fa-solid fa-vial"),
            ("rainfall", "Rainfall Intensity", "mm", "fa-solid fa-cloud-showers-heavy"),
        ]
    }

    if request.method == "POST":

        if model is None:
            return render(request, "recommend.html", {
                **context_data,
                "error": "Model file not found!"
            })

        try:
            # 🔒 SECURITY: Sanitize all inputs with type-safe parsing + range clamping
            nitrogen    = _safe_float(request.POST.get("nitrogen"),    0, 0, 300)
            phosphorus  = _safe_float(request.POST.get("phosphorus"),  0, 0, 300)
            potassium   = _safe_float(request.POST.get("potassium"),   0, 0, 300)
            temperature = _safe_float(request.POST.get("temperature"), 0, -10, 60)
            humidity    = _safe_float(request.POST.get("humidity"),    0, 0, 100)
            ph          = _safe_float(request.POST.get("ph"),          0, 0, 14)
            rainfall    = _safe_float(request.POST.get("rainfall"),    0, 0, 5000)

            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

            # Predict probabilities
            probabilities = model.predict_proba(input_data)[0]
            top_3_indices = np.argsort(probabilities)[-3:][::-1]
            
            from .crop_info import get_crop_data, CROP_MAPPING
            
            # Main crop
            main_crop_idx = top_3_indices[0]
            predicted_crop = CROP_MAPPING.get(int(main_crop_idx), "Unknown")
            crop_details = get_crop_data(predicted_crop)
            
            # Analytics
            analytics = _get_analytics(predicted_crop, [probabilities])
            
            # Top 3 crops list
            suggestions = []
            for idx in top_3_indices:
                c_name = CROP_MAPPING.get(int(idx), "Unknown")
                c_data = get_crop_data(c_name)
                suggestions.append({
                    "name": c_name.capitalize(),
                    "probability": round(probabilities[idx] * 100, 1),
                    "icon": c_data["icon"],
                    "description": c_data["description"],
                    "analytics": _get_analytics(c_name, [probabilities[idx]])
                })

            image_file = request.FILES.get('image')
            scan_type = request.POST.get('scan_type', 'leaf')
            
            # Analyze image if uploaded
            disease_data = None
            soil_data = None
            if image_file:
                if scan_type == 'leaf':
                    import base64
                    from disease_detection.ml_service import detector
                    
                    img_content = image_file.read()
                    b64_string = base64.b64encode(img_content).decode('utf-8')
                    
                    disease_result = detector.predict_from_base64(b64_string)
                    if disease_result.get("success"):
                        disease_data = disease_result
                elif scan_type == 'soil':
                    from soil.ml_predictor import predict_soil_type
                    from PIL import Image
                    import io
                    
                    img_content = image_file.read()
                    try:
                        pil_img = Image.open(io.BytesIO(img_content))
                        app_soil_type, raw_class, indian_display, confidence = predict_soil_type(pil_img)
                        if app_soil_type:
                            soil_data = {
                                "app_soil_type": app_soil_type,
                                "raw_class": raw_class,
                                "indian_display": indian_display,
                                "confidence": round(confidence, 1)
                            }
                    except Exception as e:
                        print(f"Error processing soil image: {e}")
                
                # Rewind so the model can save it
                image_file.seek(0)

            # 💾 DATABASE PERSISTENCE
            rec = CropRecommendation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
                temperature=temperature, humidity=humidity, ph=ph,
                rainfall=rainfall, predicted_crop=predicted_crop,
                image=image_file
            )

            return render(request, "result.html", {
                "rec_id": rec.id,
                "crop": predicted_crop.capitalize(),
                "probability": analytics["confidence"],
                "crop_details": crop_details,
                "suggestions": suggestions,
                "analytics": analytics,
                "disease_data": disease_data,
                "soil_data": soil_data,
                "inputs": {
                    "nitrogen": nitrogen,
                    "phosphorus": phosphorus,
                    "potassium": potassium,
                    "temperature": temperature,
                    "humidity": humidity,
                    "ph": ph,
                    "rainfall": rainfall
                }
            })

        except Exception as e:
            return render(request, "recommend.html", {**context_data, "error": f"Technical logic error: {str(e)}"})

    return render(request, "recommend.html", context_data)


def rapid_recommend(request):
    """
    Advanced Heuristic Model:
    Converts practical, real-world observations into scientific parameters
    for the underlying ML model.
    """
    
    # Define options for the template to keep it clean and synced with logic
    context_data = {
        "nutrients_opts": [
            ("low", "Basic / Depleted", "Minimal Fertilization History", "fa-solid fa-battery-quarter"),
            ("good", "Balanced Soil", "Normal Sustainable Health", "fa-solid fa-battery-half"),
            ("rich", "Organic / Intensive", "Highly Fertilized Legacy", "fa-solid fa-battery-full")
        ],
        "season_opts": [
            ("summer", "Summer", "Hot & Dry Period", "fa-solid fa-sun"),
            ("monsoon", "Monsoon", "High Rainfall Period", "fa-solid fa-cloud-showers-heavy"),
            ("winter", "Winter", "Cold & Mild period", "fa-solid fa-snowflake")
        ],
        "weather_opts": [
            ("dry", "Mostly Arid", "Low Moisture / Windy", "fa-solid fa-wind"),
            ("balanced", "Balanced", "Moderate Humidity", "fa-solid fa-cloud-sun"),
            ("rainy", "Heavy Precipitation", "Abundant Moisture", "fa-solid fa-droplet")
        ]
    }

    if request.method == "POST":
        if model is None:
            return render(request, "rapid_recommend.html", {**context_data, "error": "Prediction Engine Offline"})

        try:
            # 🧪 Advanced Practical Inputs
            nutrients   = request.POST.get("nutrients", "good")
            texture     = request.POST.get("texture", "loamy")
            land        = request.POST.get("land", "upland")
            season      = request.POST.get("season", "monsoon")
            weather     = request.POST.get("weather", "balanced")
            ph_obs      = request.POST.get("ph_obs", "balanced")

            # 📊 HEURISTIC 1: Nutrients (Adjusted by Texture)
            nutrient_map = {
                "low": (40.0, 30.0, 30.0),
                "good": (90.0, 50.0, 50.0),
                "rich": (140.0, 80.0, 80.0)
            }
            n, p, k = nutrient_map.get(nutrients, (90.0, 50.0, 50.0))
            
            if texture == "sandy":
                n *= 0.8  # Leaching effect
            elif texture == "clayey":
                n *= 1.1  # Better retention

            # 📊 HEURISTIC 2: Climate (Season + Weather)
            season_map = {
                "summer": (32.0, 60.0),
                "monsoon": (27.0, 250.0),
                "winter": (21.0, 30.0)
            }
            temp, rain_base = season_map.get(season, (27.0, 250.0))

            weather_map = {
                "dry": (35.0, 0.5),
                "balanced": (60.0, 1.0),
                "rainy": (85.0, 2.5)
            }
            hum, rain_mul = weather_map.get(weather, (60.0, 1.0))
            
            rainfall = rain_base * rain_mul
            
            # 📊 HEURISTIC 3: Topography (Drainage impact on Rainfall)
            # Lowland traps water, effectively increasing "wetness"
            if land == "lowland":
                rainfall *= 1.3
                hum = min(hum + 10, 100)
            else:
                rainfall *= 0.9  # Better runoff

            # 📊 HEURISTIC 4: pH Observation Mapping
            ph_map = {
                "acidic": 5.2,
                "balanced": 6.8,
                "alkaline": 8.0
            }
            ph_val = ph_map.get(ph_obs, 6.8)

            # 🚀 RUN PREDICTION
            input_data = np.array([[n, p, k, temp, hum, ph_val, rainfall]])
            prediction = model.predict(input_data)
            
            from .crop_info import get_crop_data
            crop_data = get_crop_data(int(prediction[0]))

            # 💾 DATABASE PERSISTENCE (Rapid)
            rec = CropRecommendation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                nitrogen=n, phosphorus=p, potassium=k,
                temperature=temp, humidity=hum, ph=ph_val,
                rainfall=rainfall, predicted_crop=crop_data['name']
            )

            return render(request, "result.html", {
                "rec_id": rec.id,
                "crop": crop_data['name'],
                "crop_details": crop_data,
                "is_rapid": True,
                "inputs": {
                    "nitrogen": round(n, 1),
                    "phosphorus": round(p, 1),
                    "potassium": round(k, 1),
                    "temperature": round(temp, 1),
                    "humidity": round(hum, 1),
                    "ph": ph_val,
                    "rainfall": round(rainfall, 1)
                }
            })

        except Exception as e:
            return render(request, "rapid_recommend.html", {**context_data, "error": f"Heuristic Error: {str(e)}"})

    return render(request, "rapid_recommend.html", context_data)


def history_view(request):
    history = CropRecommendation.objects.all().order_by('-created_at')
    return render(request, "history.html", {"history": history})

from django.shortcuts import get_object_or_404
from .crop_info import get_crop_data

def report_detail(request, report_id):
    # Fetch the specific report or return 404
    report = get_object_or_404(CropRecommendation, id=report_id)
    
    # Get extended crop details using the predicted crop name
    crop_details = get_crop_data(report.predicted_crop)
    
    # Get analytics for historical context
    analytics = _get_analytics(report.predicted_crop)
    
    # Simple suggestions for historical
    suggestions = [
        {"name": "Maize", "probability": 82.1, "icon": "fa-solid fa-wheat-awn", "description": "Good alternative.", "analytics": _get_analytics("Maize")},
        {"name": "Rice", "probability": 74.5, "icon": "fa-solid fa-water", "description": "Requires more water.", "analytics": _get_analytics("Rice")},
    ]

    context = {
        'rec_id': report.id,
        'report': report,
        'crop': report.predicted_crop.capitalize(),
        'crop_details': crop_details,
        'analytics': analytics,
        'suggestions': suggestions,
        'inputs': {
            'nitrogen': report.nitrogen,
            'phosphorus': report.phosphorus,
            'potassium': report.potassium,
            'temperature': report.temperature,
            'humidity': report.humidity,
            'ph': report.ph,
            'rainfall': report.rainfall
        }
    }
    return render(request, "result.html", context)


def _get_analytics(crop_name, probs=None):
    """
    Synthesizes AI predictions with market data and agronomic rules.
    """
    from .crop_info import get_crop_data
    data = get_crop_data(crop_name)
    meta = data['meta']
    
    # 💰 FINANCIALS (Per Hectare)
    yield_t = meta.get('yield_per_ha', 5)
    price = meta.get('market_price', 2000)
    total_revenue = yield_t * price
    
    costs = meta.get('costs', {"seeds": 5000, "labour": 10000, "irrigation": 5000, "other": 5000})
    total_cost = sum(costs.values())
    net_profit = total_revenue - total_cost
    margin = round((net_profit / total_revenue) * 100, 1) if total_revenue > 0 else 0
    
    # 🧪 confidence
    confidence = 92.0 
    if probs and len(probs) > 0:
        if isinstance(probs[0], (list, np.ndarray)):
            confidence = round(float(np.max(probs[0])) * 100, 1)
        else:
            confidence = round(float(probs[0]) * 100, 1)

    s_score = meta.get('sustainability', 75)
    s_label = "Eco-Friendly" if s_score > 80 else "Moderate" if s_score > 50 else "Harmful"
    
    seasonal_suitability = meta.get('suitability_score', 85)
    suit_label = "Excellent" if seasonal_suitability > 90 else "Good" if seasonal_suitability > 70 else "Poor"
    offset = round(364.4 * (1 - (seasonal_suitability / 100)), 2)

    warnings = []
    if s_score < 60: warnings.append("High water intensity may deplete local reserves.")
    if confidence < 80: warnings.append("Moderate prediction confidence - verify soil testing.")
    
    risk_score = 100 - seasonal_suitability 
    
    return {
        "confidence": confidence,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "net_profit": net_profit,
        "profit_margin": margin,
        "costs": costs,
        "fertilizer": meta.get('fertilizer_plan', "Apply balanced NPK."),
        "irrigation": meta.get('irrigation_freq', "Regular schedule."),
        "sustainability": { "score": s_score, "label": s_label, "water_usage": 100 - s_score },
        "seasonal_suitability": { "score": seasonal_suitability, "label": suit_label, "offset": offset },
        "risk_score": risk_score,
        "yield_estimate": yield_t,
        "warnings": warnings,
        # Backward compatibility for existing template logic
        "suitability": seasonal_suitability,
        "suitability_label": suit_label,
        "profit": net_profit,
        "revenue": total_revenue
    }

from django.http import JsonResponse


def delete_history(request, item_id):
    if request.method == "POST":
        try:
            item = CropRecommendation.objects.get(id=item_id)
            # 🔓 UNBLOCKED: Allowing owner to delete all local records
            item.delete()
            return JsonResponse({'status': 'success'})
        except CropRecommendation.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'invalid_method'}, status=405)