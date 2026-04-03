from django.shortcuts import render
import os
import json
import re
import time
from PIL import Image
from dotenv import load_dotenv
from .recommendations import SOIL_DATA
from recommend.crop_info import get_crop_data

load_dotenv()

try:
    import google.generativeai as genai
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
            # Resize image to save bandwidth and stay within API limits
            img.thumbnail((800, 800))
            
            result_class = "Analysis Failed"
            confidence = 0.0
            characteristics = ["Unable to analyze soil at this moment."]
            recommended_crops = []
            ideal_weather = None
            tips = ""
            
            token = os.getenv("GEMINI_API_KEY")
            if token and GEMINI_AVAILABLE:
                genai.configure(api_key=token)
                
                # ULTIMATE QUOTA-RESISTANT FALLBACK CHAIN FOR VISION
                model_names = [
                    'gemini-1.5-flash-8b', 
                    'gemini-flash-lite-latest',
                    'gemini-1.5-flash',
                    'gemma-3-4b-it'
                ]
                
                prompt = """
                Analyze this image. 
                1. If the image is NOT clearly a photo of soil/ground (e.g., if it's a person, a leaf, a car, or a building), respond: {"type": "Invalid", "confidence": 100.0}
                2. If it IS soil, identify the primary type from these 6 categories ONLY: [Sandy, Clay, Loamy, Silty, Peaty, Chalky].
                
                Respond strictly in this JSON format:
                {"type": "TheMatchedType", "confidence": 95.5}
                """
                
                success = False
                last_error = ""
                
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        response = model.generate_content([prompt, img], request_options={"timeout": 20})
                        
                        if response and response.text:
                            # Extract JSON
                            json_str = response.text
                            match = re.search(r'\{.*\}', json_str, re.DOTALL)
                            if match:
                                json_str = match.group(0)
                                
                            data = json.loads(json_str)
                            type_extracted = data.get("type", "Unknown")
                            confidence = float(data.get("confidence", 0.0))
                            
                            if type_extracted == "Invalid":
                                result_class = "Invalid Image Detected"
                                characteristics = ["The uploaded photo does not appear to be soil. Please upload a clear photo of the ground for accurate analysis."]
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
                            elif type_extracted == "Unknown":
                                result_class = "Not Recognized as Soil"
                                characteristics = ["The uploaded image does not appear to be recognized soil. Please try again with a clear photo."]
                                success = True
                                break
                    except Exception as e:
                        print(f"SOIL FALLBACK DEBUG: {m_name} failed: {str(e)[:100]}")
                        last_error = str(e)
                        continue
                
                if not success:
                    result_class = "Service Busy"
                    characteristics = [f"Our AI specialists are currently at capacity. Please try again in 30 seconds. 🚜"]
                    # If it was a quota error specifically, show a cleaner message
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
                "image_name": uploaded_file.name
            }
            
            return render(request, "soil_result.html", context)
            
        except Exception as e:
            return render(request, "soil_upload.html", {"error": f"Upload Error: {str(e)}"})

    return render(request, "soil_upload.html")
