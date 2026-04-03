import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_service import detector

def scan_page(request):
    """
    Renders the frontend page with the camera UI.
    """
    return render(request, 'disease_scan.html')

@csrf_exempt
def predict_disease_api(request):
    """
    API Endpoint. 
    Accepts POST requests with a JSON payload containing 'image_data' (Base64).
    Returns JSON with disease prediction.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            b64_img = body.get('image_data')

            if not b64_img:
                return JsonResponse({"error": "No image data provided"}, status=400)

            # Pass the base64 string to our ML service
            result = detector.predict_from_base64(b64_img)

            if result.get("success"):
                return JsonResponse({
                    "success": True,
                    "disease": result["disease"],
                    "confidence": result["confidence"],
                    "description": result["description"],
                    "treatment": result["treatment"],
                    "prevention": result["prevention"]
                })
            else:
                return JsonResponse({"error": result.get("error", "Prediction failed")}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)
