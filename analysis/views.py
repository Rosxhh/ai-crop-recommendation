import os
import json
import re
import joblib  # type: ignore
import numpy as np  # type: ignore
from PIL import Image  # type: ignore
from django.shortcuts import render  # type: ignore
from django.conf import settings  # type: ignore
from recommend.crop_info import get_crop_data  # type: ignore
from soil.recommendations import SOIL_DATA  # type: ignore
from dotenv import load_dotenv  # type: ignore
from .ai_logic import get_agronomist_strategy
from django.http import JsonResponse
from .models import DiseaseMarker

load_dotenv()

try:
    import google.generativeai as genai  # type: ignore
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Load Models
crop_model_path = os.path.join(settings.BASE_DIR, "crop1.pkl")
yield_model_path = os.path.join(settings.BASE_DIR, "yield_model.pkl")

try:
    crop_model = joblib.load(crop_model_path)
    yield_model = joblib.load(yield_model_path)
except Exception as e:
    print(f"Error loading ML models: {e}")
    crop_model = None
    yield_model = None

REGION_DATA = {
    "north": {"N": 100, "P": 50, "K": 40, "temperature": 25.0, "humidity": 60.0, "ph": 7.0, "rainfall": 80.0},
    "south": {"N": 80, "P": 40, "K": 50, "temperature": 30.0, "humidity": 85.0, "ph": 6.8, "rainfall": 200.0},
    "east": {"N": 85, "P": 45, "K": 40, "temperature": 28.0, "humidity": 80.0, "ph": 6.2, "rainfall": 180.0},
    "west": {"N": 70, "P": 50, "K": 45, "temperature": 32.0, "humidity": 55.0, "ph": 6.8, "rainfall": 70.0},
    "central": {"N": 90, "P": 45, "K": 40, "temperature": 29.0, "humidity": 65.0, "ph": 7.2, "rainfall": 100.0},
}

SOIL_NUTRIENT_MULTIPLIERS = {
    "Sandy": {"N": 0.4, "P": 0.5, "K": 0.5, "humidity": 0.7},
    "Clay": {"N": 1.1, "P": 1.2, "K": 1.1, "humidity": 1.2},
    "Loamy": {"N": 1.0, "P": 1.0, "K": 1.0, "humidity": 1.0},
    "Silty": {"N": 0.8, "P": 0.9, "K": 0.9, "humidity": 1.1},
    "Peaty": {"N": 1.3, "P": 0.6, "K": 0.6, "humidity": 1.3},
    "Chalky": {"N": 0.6, "P": 0.7, "K": 0.8, "humidity": 0.6},
}

# -------------------------------------------------------
# 🧠 PREMIUM FEATURE HELPERS
# -------------------------------------------------------

def calculate_fertilizer(current_npk, ideal_npk, area):
    """
    Calculates Urea, DAP, and MOP required in kg for a given area.
    Formula: Gap = Ideal - Current. 
    Urea (46% N), DAP (18% N, 46% P), MOP (60% K).
    """
    n_gap = float(max(0.0, float(ideal_npk[0]) - float(current_npk[0])))
    p_gap = float(max(0.0, float(ideal_npk[1]) - float(current_npk[1])))
    k_gap = float(max(0.0, float(ideal_npk[2]) - float(current_npk[2])))

    # DAP supplies all P and some N
    dap_needed = (p_gap / 0.46) * area
    n_from_dap = dap_needed * 0.18
    
    # Remaining N gap filled by Urea
    remaining_n = float(max(0.0, (n_gap * float(area)) - n_from_dap))
    urea_needed = remaining_n / 0.46
    
    # K gap filled by Muriate of Potash (MOP)
    mop_needed = (k_gap / 0.60) * area

    return {
        "urea": round(float(urea_needed), 1),
        "dap": round(float(dap_needed), 1),
        "mop": round(float(mop_needed), 1),
        "total_kg": round(float(urea_needed + dap_needed + mop_needed), 1)
    }

def calculate_climate_score(current, ideal_npk, temp, hum, rain, ph):
    """Calculates a compatibility score from 0-100 based on standard dev from ideal conditions."""
    # Simplified weights
    score = 100
    # Deduct for variations (Rough heuristic for academic display)
    if ph < 5.5 or ph > 7.5: score -= 15
    if rain < 50: score -= 10
    if temp > 35 or temp < 15: score -= 10
    return max(35, min(100, score))


def smart_analysis(request):
    uploaded_url = None
    if request.method == "POST" and request.FILES.get("image"):
        if not crop_model or not yield_model:
            return render(request, "smart_analysis.html", {"error": "ML Prediction models are missing."})

        try:
            area = float(request.POST.get("area") or 1.0)
            region = request.POST.get("region", "central")
            
            # Extract basic data based on region
            r_data = REGION_DATA.get(region, REGION_DATA["central"])
            n, p, k = r_data["N"], r_data["P"], r_data["K"]
            temp, hum, ph, rain = r_data["temperature"], r_data["humidity"], r_data["ph"], r_data["rainfall"]

            # Process Image for Soil Type
            uploaded_file = request.FILES["image"]
            img = Image.open(uploaded_file)
            img.thumbnail((800, 800))

            soil_type = "Unknown Analysis"
            soil_characteristics = ["Unable to completely analyze soil structure."]
            soil_confidence = 0.0
            indian_soil_name = None   
            yield_quality_multiplier = 1.0   # Baseline yield factor
            ai_tags = []                     # AI sensory labels
            indian_soil_name = None   # Indian soil display name from local model

            # ──────────────────────────────────────────────────────────────────
            # 🧠  STEP 1 — LOCAL CNN (soil_model.h5 trained on 6000 Indian soil images)
            # Uses your own trained CNN as primary engine.
            # If confidence >= 60%, no Gemini call needed → saves API quota.
            # ──────────────────────────────────────────────────────────────────
            _used_local_model = False
            try:
                from soil.ml_predictor import predict_soil_type as _local_soil_predict
                _ml_type, _ml_raw, _ml_indian, _ml_conf = _local_soil_predict(img)

                if _ml_type and _ml_conf >= 60.0 and _ml_type in SOIL_DATA:
                    soil_type            = _ml_type
                    indian_soil_name     = _ml_indian
                    soil_confidence      = _ml_conf
                    soil_characteristics = SOIL_DATA[soil_type]["characteristics"]
                    _used_local_model    = True

                    # Adjust NPK values for the detected soil type
                    multipliers = SOIL_NUTRIENT_MULTIPLIERS.get(soil_type, {"N":1,"P":1,"K":1,"humidity":1})
                    n   = round(n   * multipliers["N"],        2)
                    p   = round(p   * multipliers["P"],        2)
                    k   = round(k   * multipliers["K"],        2)
                    hum = round(hum * multipliers["humidity"], 2)
                    print(f"[Analysis] ✅ Local CNN: {_ml_raw} → {soil_type} ({_ml_conf:.1f}%)")

            except Exception as _e:
                print(f"[Analysis] Local CNN step failed: {_e}")

            # ──────────────────────────────────────────────────────────────────
            # 🤖  STEP 2 — GEMINI AI (fallback when local model < 60% confidence)
            # ──────────────────────────────────────────────────────────────────
            if not _used_local_model:
                token = os.getenv("GEMINI_API_KEY")
                if token and GEMINI_AVAILABLE:
                    genai.configure(api_key=token)
                    model_names = ['gemini-1.5-flash-8b', 'gemini-flash-lite-latest', 'gemini-1.5-flash', 'gemma-3-4b-it']

                    prompt = """Analyze this soil image in extreme detail for agricultural purposes.
                    1. If the image is NOT clearly a photo of soil/earth, respond: {"type": "Invalid", "confidence": 100}
                    2. If it IS soil:
                       - "type": Choose one from [Sandy, Clay, Loamy, Silty, Peaty, Chalky].
                       - "confidence": confidence percentage.
                       - "texture": One of [Fine, Course, Clumpy, Loose].
                       - "color": One of [Black/Dark, Red, Brown, Yellow, Pale].
                       - "moisture": One of [Dry, Moist, Saturated].
                       - "organic_matter": One of [High, Medium, Low].
                       - "ph_estimate": A scientific estimate of pH (4.5 - 8.5) based on soil type and color.
                       - "regional_name": The specific Indian regional name for this soil (e.g., "Black Cotton Soil", "Kallar", "Regur").
                       - "top_crops": List 3 specific crops suited for these visual conditions.
                       - "best_practices": [3-sentence professional "Dos"].
                       - "bad_practices": [3-sentence professional "Don'ts"].

                    Respond strictly in JSON format like: 
                    {"type": "Loamy", "confidence": 98, "texture": "Fine", "color": "Dark", "moisture": "Moist", "organic_matter": "High", "ph_estimate": 6.8, "regional_name": "Alluvial Soil", "top_crops": ["Wheat", "Potato", "Tomato"], "best_practices": ["Rotate crops regularly", "Add organic mulch", "Monitor pH"], "bad_practices": ["Avoid over-tilling", "Don't use chemical-heavy fertilizers", "Avoid walking on wet soil"]}"""

                    for m_name in model_names:
                        try:
                            g_model = genai.GenerativeModel(m_name)
                            response = g_model.generate_content([prompt, img], request_options={"timeout": 20})
                            if response and response.text:
                                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                                if match:
                                    data = json.loads(match.group(0))
                                    extracted = data.get("type", "Unknown")
                                    if extracted == "Invalid":
                                        soil_type = "Wrong Image Type"
                                        soil_characteristics = ["The uploaded image does not appear to be soil. Please upload a clear photo of the ground."]
                                        soil_confidence = 100.0
                                        break
                                    elif extracted in SOIL_DATA:
                                        soil_type = extracted
                                        indian_soil_name = data.get("regional_name", extracted)
                                        soil_confidence = float(data.get("confidence", 0.0))
                                        ai_sensing = {
                                            "texture": data.get("texture", "Mixed"),
                                            "color": data.get("color", "Varies"),
                                            "moisture": data.get("moisture", "Detected"),
                                            "organic": data.get("organic_matter", "Medium"),
                                            "ph": float(data.get("ph_estimate", ph)),
                                            "crops": data.get("top_crops", []),
                                            "dos": data.get("best_practices", []),
                                            "donts": data.get("bad_practices", [])
                                        }
                                        soil_characteristics = SOIL_DATA[extracted]["characteristics"]
                                        ph = ai_sensing["ph"]
                                        
                                        # Advanced NPK Multiplier based on AI Sensing
                                        multipliers = SOIL_NUTRIENT_MULTIPLIERS.get(soil_type, {"N":1,"P":1,"K":1,"humidity":1})
                                        n_factor = multipliers["N"]
                                        if ai_sensing["organic"] == "High": n_factor *= 1.2
                                        if ai_sensing["moisture"] == "Saturated": n_factor *= 0.8 # leaching risk
                                        
                                        n   = round(n   * n_factor, 2)
                                        p   = round(p   * multipliers["P"], 2)
                                        k   = round(k   * multipliers["K"], 2)
                                        hum = round(hum * multipliers["humidity"], 2)
                                        
                                        # Yield Adjustment based on visual health
                                        if ai_sensing["organic"] == "High" and ai_sensing["moisture"] == "Moist":
                                            yield_quality_multiplier = 1.15
                                        elif ai_sensing["moisture"] == "Dry":
                                            yield_quality_multiplier = 0.85
                                        else:
                                            yield_quality_multiplier = 1.0
                                            
                                        break
                        except Exception:
                            continue

            # Market Price Data (INR per Ton)
            MARKET_PRICES = {
                "rice": 22000, "maize": 19000, "jute": 45000, "cotton": 65000,
                "coconut": 38000, "papaya": 28000, "orange": 48000, "apple": 85000,
                "muskmelon": 22000, "watermelon": 16000, "grapes": 55000, "mango": 42000,
                "banana": 18000, "pomegranate": 75000, "lentil": 68000, "blackgram": 62000,
                "mungbean": 72000, "mothbeans": 58000, "pigeonpeas": 78000, "kidneybeans": 82000,
                "chickpea": 55000, "coffee": 180000
            }

            # Crop ML Model
            crop_input = np.array([[n, p, k, temp, hum, ph, rain]])
            crop_pred = int(crop_model.predict(crop_input)[0])  # type: ignore
            crop_info = get_crop_data(crop_pred)
            crop_name_lower = crop_info['name'].lower()

            # --- OVERRIDE WITH AI SOIL ANALYSIS ---
            if soil_type in SOIL_DATA and len(SOIL_DATA[soil_type].get("crops", [])) > 0:
                ai_crop_name = SOIL_DATA[soil_type]["crops"][0].lower()
                crop_info = get_crop_data(ai_crop_name)
                crop_name_lower = crop_info['name'].lower()

            # Yield ML Model
            yield_input = np.array([[n, p, k, temp, hum, ph, rain, area]])
            total_yield = round(float(yield_model.predict(yield_input)[0]) * yield_quality_multiplier, 2)  # type: ignore
            yield_ph = round(total_yield / area, 2) if area > 0 else 0  # type: ignore

            # Calculate Market Value
            price_per_ton = MARKET_PRICES.get(crop_name_lower, 25000)
            market_value = round(total_yield * price_per_ton, 2)
            
            # Water requirement estimation (mm to Liters conversion for area)
            # 1mm rainfall = 10,000 Liters per Hectare
            water_needed = int(rain * 10000 * area) if rain else 0

            # 🧪 Fertilizer Prescription
            ideal_npk = crop_info['meta'].get('ideal_npk', [100, 50, 50])
            fertilizers = calculate_fertilizer([n, p, k], ideal_npk, area)
            
            # 🌡️ Climate Compatibility
            climate_score = calculate_climate_score([n,p,k], ideal_npk, temp, hum, rain, ph)

            # 📅 Growth Timeline
            from datetime import datetime, timedelta
            harvest_days = crop_info['meta'].get('growth_days', 120)
            harvest_date = (datetime.now() + timedelta(days=harvest_days)).strftime("%d %b %Y")

            # 🤖 AI Agronomist (Contextual Insights)
            ai_advice = get_agronomist_strategy(soil_type, temp, hum)

            # 📈 ROI Market Battle (Economic Comparison)
            # Pick 2 alternative crops based on price/yield similarity or just diverse options
            alt_names = ["maize", "jute"] if crop_name_lower == "rice" else ["rice", "maize"]
            alternatives = []
            for alt_name in alt_names:
                alt_price = MARKET_PRICES.get(alt_name, 25000)
                # Simple estimate: same yield for comparison or 80% if not expert
                alt_revenue = round(total_yield * alt_price * 0.9, 2) 
                alternatives.append({"name": alt_name.capitalize(), "revenue": alt_revenue})

            # Generate dynamic recommendations (Top 4 including predicted)
            recommended_crops = []
            
            # Priority 1: Crops specifically suited for the detected Soil Type
            if soil_type in SOIL_DATA:
                soil_specific_crops = [c.lower() for c in SOIL_DATA[soil_type].get("crops", [])]
                for sc in soil_specific_crops:
                    if sc not in recommended_crops:
                        recommended_crops.append(sc)
            
            # Priority 2: Add the predicted baseline crop if not already present
            if crop_name_lower not in recommended_crops:
                recommended_crops.append(crop_name_lower)
                
            # Fill the remainder with diverse alternatives to ensure 4 options
            for alt_name in MARKET_PRICES.keys():
                if alt_name not in recommended_crops:
                    recommended_crops.append(alt_name)
                if len(recommended_crops) >= 4:
                    break
            
            recommended_crops = recommended_crops[:4]

            # Collect AI sensory tags and maintenance
            ai_tags = []
            best_practices = []
            bad_practices = []
            if 'ai_sensing' in locals():
                ai_tags = [
                    f"Texture: {ai_sensing['texture']}",
                    f"Color: {ai_sensing['color']}",
                    f"Moisture: {ai_sensing['moisture']}",
                    f"Health: {ai_sensing['organic']} Organic"
                ]
                best_practices = ai_sensing.get('dos', [])
                bad_practices = ai_sensing.get('donts', [])

            context = {
                "result_ready": True,
                "result_class": soil_type,
                "indian_soil_name": indian_soil_name,  # e.g. "Alluvial Soil" from local CNN
                "characteristics": soil_characteristics,
                "soil_confidence": soil_confidence,
                "uploaded_url": uploaded_url,
                "crop": crop_info['name'],
                "crop_details": crop_info,
                "yield": total_yield,
                "yield_ph": yield_ph,
                "market_value": market_value,
                "price_per_ton": price_per_ton,
                "water_needed": water_needed,
                "region": region.capitalize(),
                "area": area,
                "fertilizers": fertilizers,
                "climate_score": climate_score,
                "harvest_days": harvest_days,
                "harvest_date": harvest_date,
                "ai_insights": ai_advice,
                "ai_tags": ai_tags,
                "best_practices": best_practices,
                "bad_practices": bad_practices,
                "recommended_crops": recommended_crops,
                "alternatives": alternatives,
                "temperature": temp,
                "humidity": hum,
                "ph": ph,
                "rainfall": rain,
                "inputs": {
                    "nitrogen": n,
                    "phosphorus": p,
                    "potassium": k,
                }
            }

            return render(request, "smart_analysis.html", context)

        except Exception as e:
            return render(request, "smart_analysis.html", {"error": f"Failed to analyze: {str(e)}"})

    return render(request, "smart_analysis.html")

def disease_scan(request):
    if request.method == "POST" and request.FILES.get("image"):
        try:
            uploaded_file = request.FILES["image"]
            # Save or process for display (using temporary storage or base64)
            # For this dashboard, we'll pass the file directly to the context if simple, 
            # but usually we save it first.
            from django.core.files.storage import default_storage
            temp_path = default_storage.save(f"tmp/{uploaded_file.name}", uploaded_file)
            uploaded_url = default_storage.url(temp_path)
            img = Image.open(uploaded_file)
            img.thumbnail((800, 800))
            
            token = os.getenv("GEMINI_API_KEY")
            if not token or not GEMINI_AVAILABLE:
                return render(request, "disease_scan.html", {"error": "AI Vision API not configured."})
                
            genai.configure(api_key=token)
            model_names = ['gemini-1.5-flash-8b', 'gemini-flash-lite-latest', 'gemini-1.5-flash', 'gemma-3-4b-it']
            
            prompt = """Analyze this image.
            1. If the image is NOT clearly a plant leaf or foliage (e.g., if it's soil, a person, or a non-living object), respond: {"crop": "Invalid", "disease": "Invalid", "confidence": 100.0, "treatment_organic": "N/A", "treatment_chemical": "N/A", "risk_level": "None"}
            2. If it IS a leaf, identify the crop and any visible disease.
            
            Respond strictly in this JSON format:
            {"crop": "Tomato", "disease": "Early Blight", "confidence": 95.5, "treatment_organic": "Apply copper-based fungicide", "treatment_chemical": "Chlorothalonil spray", "risk_level": "High"}"""
            
            for m_name in model_names:
                try:
                    g_model = genai.GenerativeModel(m_name)  # type: ignore
                    response = g_model.generate_content([prompt, img], request_options={"timeout": 20})  # type: ignore
                    if response and response.text:
                        match = re.search(r'\{.*\}', response.text, re.DOTALL)
                        if match:
                            data = json.loads(match.group(0))
                            crop_detected = data.get("crop", "Unknown")
                            if crop_detected == "Invalid":
                                context = {
                                    "result": "Invalid",
                                    "crop": "Incorrect Image Type",
                                    "disease": "Soil/Non-Leaf Image Detected",
                                    "confidence": 100.0,
                                    "organic": "Please upload a clear photo of an infected leaf. It looks like you uploaded soil or a non-plant object.",
                                    "chemical": "Switch to 'Smart Vision Analysis' if you want to analyze soil samples.",
                                    "risk": "N/A"
                                }
                                return render(request, "disease_scan.html", context)
                                
                            context = {
                                "result": True,
                                "crop": crop_detected,
                                "disease": data.get("disease", "Unknown Error"),
                                "confidence": float(data.get("confidence", 0.0)),
                                "organic": data.get("treatment_organic", "None identified"),
                                "chemical": data.get("treatment_chemical", "None identified"),
                                "risk": data.get("risk_level", "Unknown")
                            }
                            return render(request, "disease_scan.html", context)
                except Exception:
                    continue
                    
            return render(request, "disease_scan.html", {"error": "AI models failed to analyze the image."})
            
        except Exception as e:
            return render(request, "disease_scan.html", {"error": f"Analysis failed: {str(e)}"})
            
    return render(request, "disease_scan.html")

def disease_markers_api(request):
    """API endpoint to return all disease markers for the Leaflet map."""
    markers = DiseaseMarker.objects.all()
    data = [
        {
            "id": m.id,
            "name": m.disease_name,
            "lat": m.latitude,
            "lng": m.longitude,
            "date": m.report_date.strftime("%Y-%m-%d")
        } for m in markers
    ]
    return JsonResponse({"markers": data})
