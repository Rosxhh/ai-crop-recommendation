from django.shortcuts import render
import os
import json
import re
import time
from PIL import Image
from dotenv import load_dotenv
from .recommendations import SOIL_DATA
from recommend.crop_info import get_crop_data
# ml_predictor is imported inline inside the try-block below

load_dotenv()

try:
    from ..ai import free_ai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def soil_predict(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]
        try:
            # 🔒 SECURITY: Validate file type by extension (whitelist)
            ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
            ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else ''
            if ext not in ALLOWED_EXTENSIONS:
                return render(request, "soil_upload.html", {
                    "error": "Invalid file type. Please upload a JPG, JPEG, PNG, or WEBP image."
                })

            # 🔒 SECURITY: Enforce 10MB upload size limit
            MAX_SIZE = 10 * 1024 * 1024  # 10 MB in bytes
            if uploaded_file.size > MAX_SIZE:
                return render(request, "soil_upload.html", {
                    "error": "File too large. Please upload an image smaller than 10MB."
                })

            img = Image.open(uploaded_file)
            
            # Convert uploaded image to base64 to display on the result page
            import base64
            from io import BytesIO
            img_byte_arr = BytesIO()
            img_format = img.format if img.format else 'JPEG'
            # Convert to RGB if format is JPEG to avoid errors with RGBA
            if img_format == 'JPEG' and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(img_byte_arr, format=img_format)
            img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            img_data_uri = f"data:image/{img_format.lower()};base64,{img_b64}"

            # Resize image to save bandwidth and stay within API limits
            img.thumbnail((800, 800))
            
            result_class = "Scout Analysis Failed"
            confidence = 0.0
            characteristics = ["Unable to analyze soil at this moment."]
            recommended_crops = []
            ideal_weather = None
            tips = ""
            indian_soil_name = None   # Indian soil display name from local model
            used_local_model = False  # Track which engine was used

            # ──────────────────────────────────────────────────────────────
            # 🧠  STEP 1 — LOCAL CNN (soil_model.h5 trained on 6000 images)
            # Runs first. If confidence >= 60%, skip Gemini entirely.
            # ──────────────────────────────────────────────────────────────
            try:
                from .ml_predictor import predict_soil_type
                ml_type, ml_raw, ml_indian, ml_conf = predict_soil_type(img)

                if ml_type and ml_conf >= 60.0 and ml_type in SOIL_DATA:
                    result_class     = ml_type
                    indian_soil_name = ml_indian
                    confidence       = ml_conf
                    used_local_model = True
                    soil_info        = SOIL_DATA[result_class]
                    characteristics  = soil_info["characteristics"]
                    recommended_crops = soil_info["crops"]
                    ideal_weather    = soil_info.get("ideal_weather", None)
                    tips             = soil_info["tips"]
                    print(f"[SoilML] ✅ Local model: {ml_raw} → {result_class} ({ml_conf:.1f}%)")

            except Exception as e:
                print(f"[SoilML] Local model step failed: {e}")

            if used_local_model:
            
                pass  # Local model succeeded — no Gemini needed

            # ──────────────────────────────────────────────────────────────
            # 🤖  STEP 2 — GEMINI AI (fallback when local model < 60% conf)
            # ──────────────────────────────────────────────────────────────
            else:
                token = os.getenv("GEMINI_API_KEY")
                if token and GEMINI_AVAILABLE:
                    genai.configure(api_key=token)
                    model_names = [
                        'gemini-1.5-flash-8b',
                        'gemini-flash-lite-latest',
                        'gemini-1.5-flash',
                        'gemma-3-4b-it'
                    ]
                    prompt = """
                    Analyze this image.
                    1. If the image is NOT clearly soil/ground, respond: {"type": "Invalid", "confidence": 100.0}
                    2. If it IS soil, identify the primary type from: [Sandy, Clay, Loamy, Silty, Peaty, Chalky].
                    Respond strictly: {"type": "TheMatchedType", "confidence": 95.5}
                    """
                    success = False
                    last_error = ""
                    for m_name in model_names:
                        try:
                            g_model = genai.GenerativeModel(m_name)
                            response = g_model.generate_content([prompt, img], request_options={"timeout": 20})
                            if response and response.text:
                                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                                if match:
                                    data = json.loads(match.group(0))
                                    type_extracted = data.get("type", "Unknown")
                                    confidence = float(data.get("confidence", 0.0))
                                    if type_extracted == "Invalid":
                                        result_class = "Scout: Invalid Imagery"
                                        characteristics = ["The uploaded photo does not appear to be soil. Please upload a clear photo of the ground."]
                                        success = True
                                        break
                                    elif type_extracted in SOIL_DATA:
                                        result_class = type_extracted
                                        soil_info = SOIL_DATA[type_extracted]
                                        characteristics = soil_info["characteristics"]
                                        recommended_crops = soil_info["crops"]
                                        ideal_weather = soil_info.get("ideal_weather", None)
                                        tips = soil_info["tips"]
                                        success = True
                                        break
                        except Exception as e:
                            last_error = str(e)
                            continue
                    if not success:
                        result_class = "Scout System Busy"
                        characteristics = ["AI systems are under heavy load. Please try again in 30 seconds. 🌾"]
                        if "429" in last_error:
                            characteristics = ["Agricultural AI systems are under heavy load. Retrying in 30 seconds... 🌾"]
                else:
                    result_class = "Configuration Error"
                    characteristics = ["AI access not configured. Please check API settings."]
            
            # Get detailed crop data for recommendations
            rich_crops = [get_crop_data(crop) for crop in recommended_crops]

            context = {
                "result": result_class,
                "confidence": f"{confidence:.1f}%",
                "characteristics": characteristics,
                "recommended_crops": recommended_crops,
                "rich_crops": rich_crops,
                "ideal_weather": ideal_weather,
                "tips": tips,
                "image_name": uploaded_file.name,
                "uploaded_image_uri": img_data_uri,
                "indian_soil_name": indian_soil_name,  # e.g. "Alluvial Soil"
                "used_local_model": used_local_model,  # True = CNN, False = Gemini
            }
            
            return render(request, "soil_result.html", context)
            
        except Exception as e:
            return render(request, "soil_upload.html", {"error": f"Upload Error: {str(e)}"})

    return render(request, "soil_upload.html")


# ─────────────────────────────────────────────────────────────────────────────
# 📡  LIVE SOIL SCAN — JSON API for real-time camera analysis
# POST /soil/live/  →  { image_data: "data:image/jpeg;base64,..." }
# Returns a JSON object with soil type + extended agronomic metrics
# ─────────────────────────────────────────────────────────────────────────────

# Agronomic metrics lookup for each soil type
# (values are reasonable scientific estimates; actual lab tests will vary)
LIVE_SOIL_METRICS = {
    "Loamy": {
        "indian_name":      "Alluvial Soil",
        "water_retention":  "High",
        "water_pct":        62,
        "ph_min":           6.0,  "ph_max": 7.0,
        "ph_label":         "Neutral (6.0 – 7.0)",
        "fertility":        "Very High",
        "fertility_score":  90,
        "drainage":         "Moderate",
        "organic_matter":   "High",
        "texture":          "Fine-grained & Crumbly",
        "color":            "#8B6914",
        "best_crops":       ["Rice", "Wheat", "Vegetables", "Sugarcane", "Maize"],
        "tip":              "Excellent base soil. Maintain with organic compost and avoid waterlogging.",
    },
    "Sandy": {
        "indian_name":      "Arid / Desert Soil",
        "water_retention":  "Very Low",
        "water_pct":        18,
        "ph_min":           5.5,  "ph_max": 7.5,
        "ph_label":         "Slightly Acidic–Neutral (5.5–7.5)",
        "fertility":        "Low",
        "fertility_score":  28,
        "drainage":         "Very Fast",
        "organic_matter":   "Low",
        "texture":          "Coarse & Gritty",
        "color":            "#C2955A",
        "best_crops":       ["Groundnut", "Watermelon", "Carrot", "Millet", "Radish"],
        "tip":              "Apply heavy organic mulch and irrigate frequently to compensate for fast drainage.",
    },
    "Clay": {
        "indian_name":      "Laterite Soil",
        "water_retention":  "Very High",
        "water_pct":        80,
        "ph_min":           5.5,  "ph_max": 7.0,
        "ph_label":         "Slightly Acidic (5.5–7.0)",
        "fertility":        "High",
        "fertility_score":  72,
        "drainage":         "Poor",
        "organic_matter":   "Moderate",
        "texture":          "Dense & Sticky",
        "color":            "#6B3A2A",
        "best_crops":       ["Cotton", "Rice", "Sugarcane", "Wheat", "Soybean"],
        "tip":              "Install drainage channels. Deep ploughing before planting improves aeration.",
    },
    "Silty": {
        "indian_name":      "Mountain / Forest Soil",
        "water_retention":  "High",
        "water_pct":        68,
        "ph_min":           6.0,  "ph_max": 7.0,
        "ph_label":         "Neutral (6.0–7.0)",
        "fertility":        "High",
        "fertility_score":  78,
        "drainage":         "Moderate to Poor",
        "organic_matter":   "Moderate–High",
        "texture":          "Smooth & Silky",
        "color":            "#7D6B52",
        "best_crops":       ["Maize", "Vegetables", "Wheat", "Soybean", "Barley"],
        "tip":              "Avoid compaction by limiting foot traffic on wet fields. Crop rotation improves structure.",
    },
    "Peaty": {
        "indian_name":      "Yellow Soil",
        "water_retention":  "Extreme",
        "water_pct":        88,
        "ph_min":           3.5,  "ph_max": 5.5,
        "ph_label":         "Acidic (3.5–5.5)",
        "fertility":        "Medium",
        "fertility_score":  52,
        "drainage":         "Very Poor",
        "organic_matter":   "Very High",
        "texture":          "Dark & Spongy",
        "color":            "#3D3018",
        "best_crops":       ["Blueberry", "Cranberry", "Potato", "Turnip"],
        "tip":              "Apply lime regularly to neutralise acidity. Drainage improvement is essential.",
    },
    "Chalky": {
        "indian_name":      "Red Soil",
        "water_retention":  "Low",
        "water_pct":        24,
        "ph_min":           7.5,  "ph_max": 8.5,
        "ph_label":         "Alkaline (7.5–8.5)",
        "fertility":        "Low–Medium",
        "fertility_score":  38,
        "drainage":         "Fast",
        "organic_matter":   "Low",
        "texture":          "Stony & Chalky",
        "color":            "#B85C38",
        "best_crops":       ["Lavender", "Spinach", "Beet", "Cabbage", "Corn"],
        "tip":              "Add organic compost to improve fertility. Iron/manganese deficiency is common—monitor leaves.",
    },
}


def live_soil_scan(request):
    """
    JSON endpoint for real-time camera soil analysis.
    Accepts: POST { "image_data": "data:image/jpeg;base64,..." }
    Returns: JSON with soil type + agronomic metrics
    """
    from django.http import JsonResponse
    import base64
    import io

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required."}, status=405)

    try:
        body   = json.loads(request.body)
        img_b64 = body.get("image_data", "")

        # Strip data URL prefix if present
        if "," in img_b64:
            img_b64 = img_b64.split(",", 1)[1]

        if not img_b64:
            return JsonResponse({"success": False, "error": "No image data received."})

        img_bytes = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.thumbnail((512, 512))   # smaller for speed

        soil_type    = None
        indian_name  = None
        confidence   = 0.0

        # ── Step 1: Local CNN ────────────────────────────────────────────
        try:
            from .ml_predictor import predict_soil_type
            ml_type, ml_raw, ml_indian, ml_conf = predict_soil_type(img)
            if ml_type and ml_conf >= 55.0 and ml_type in LIVE_SOIL_METRICS:
                soil_type   = ml_type
                indian_name = ml_indian
                confidence  = ml_conf
        except Exception as e:
            print(f"[LiveScan] CNN error: {e}")

        # ── Step 2: Gemini fallback ──────────────────────────────────────
        if not soil_type:
            token = os.getenv("GEMINI_API_KEY")
            if token and GEMINI_AVAILABLE:
                try:
                    genai.configure(api_key=token)
                    for m_name in ['gemini-1.5-flash-8b', 'gemini-1.5-flash']:
                        try:
                            g_model = genai.GenerativeModel(m_name)
                            prompt = ('Analyze this soil image. Identify the soil type from exactly '
                                      'one of: [Sandy, Clay, Loamy, Silty, Peaty, Chalky]. '
                                      'Respond ONLY as JSON: {"type":"Loamy","confidence":88.0}')
                            resp = g_model.generate_content([prompt, img], request_options={"timeout": 15})
                            if resp and resp.text:
                                m = re.search(r'\{.*\}', resp.text, re.DOTALL)
                                if m:
                                    d = json.loads(m.group(0))
                                    t = d.get("type", "")
                                    if t in LIVE_SOIL_METRICS:
                                        soil_type  = t
                                        confidence = float(d.get("confidence", 70.0))
                                        indian_name = LIVE_SOIL_METRICS[t]["indian_name"]
                                        break
                        except Exception:
                            continue
                except Exception as e:
                    print(f"[LiveScan] Gemini error: {e}")

        if not soil_type:
            return JsonResponse({"success": False, "error": "Could not identify soil type. Ensure the camera is pointing at bare soil."})

        metrics = LIVE_SOIL_METRICS[soil_type]
        return JsonResponse({
            "success":        True,
            "soil_type":      soil_type,
            "indian_name":    indian_name or metrics["indian_name"],
            "confidence":     round(confidence, 1),
            "water_retention": metrics["water_retention"],
            "water_pct":      metrics["water_pct"],
            "ph_label":       metrics["ph_label"],
            "ph_min":         metrics["ph_min"],
            "ph_max":         metrics["ph_max"],
            "fertility":      metrics["fertility"],
            "fertility_score": metrics["fertility_score"],
            "drainage":       metrics["drainage"],
            "organic_matter": metrics["organic_matter"],
            "texture":        metrics["texture"],
            "color":          metrics["color"],
            "best_crops":     metrics["best_crops"],
            "tip":            metrics["tip"],
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

