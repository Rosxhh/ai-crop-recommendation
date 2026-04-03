import base64
import os
import json

try:
    import google.generativeai as genai # type: ignore
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class DiseaseDetector:
    def __init__(self):
        pass

    def predict_from_base64(self, b64_string):
        """
        Receives a base64 encoded image string.
        Returns a dict with prediction results using Gemini Vision.
        """
        try:
            # Strip the data:image prefix if present
            if ',' in b64_string:
                b64_string = b64_string.split(',')[1]

            img_data = base64.b64decode(b64_string)

            api_key = os.getenv("GEMINI_API_KEY")
            
            # Using Gemini Vision to determine if it's a leaf and predict disease
            if api_key and HAS_GENAI:
                try:
                    genai.configure(api_key=api_key)
                    
                    prompt = """
                    Analyze this image carefully. Provide the output strictly in this JSON format:
                    {
                        "is_leaf": true/false,
                        "disease": "Disease Name or Healthy Leaf",
                        "confidence": 0-100,
                        "description": "2 sentence description of the disease/health",
                        "treatment": "1 sentence treatment plan",
                        "prevention": "1 sentence prevention plan"
                    }
                    
                    CRITICAL INSTRUCTION: If the image clearly DOES NOT contain a plant leaf, vine, or crop (for example, if it's a person, phone, random object, or blank wall), you MUST set "is_leaf" to false, and leave the other fields blank. Do not invent a disease for a human face or a random object. If it IS a leaf, try to detect any disease visible.
                    """
                    
                    model_names = [
                        "gemini-2.5-flash",
                        "gemini-flash-latest",
                        "gemini-2.0-flash",
                        "gemini-2.5-pro"
                    ]
                    
                    response = None
                    last_error = None
                    for m_name in model_names:
                        try:
                            # print(f"Trying model: {m_name}")
                            model = genai.GenerativeModel(m_name)
                            response = model.generate_content([
                                {"mime_type": "image/jpeg", "data": img_data},
                                prompt
                            ])
                            if response and response.text:
                                break
                        except Exception as inner_e:
                            last_error = inner_e
                            continue
                            
                    if not response or not response.text:
                        raise Exception(f"All vision models failed. Last error: {last_error}")
                    
                    res_text = response.text.strip()
                    if res_text.startswith("```json"):
                        res_text = res_text[7:-3]
                    elif res_text.startswith("```"):
                        res_text = res_text[3:-3]
                        
                    data = json.loads(res_text.strip())
                    
                    if not data.get("is_leaf", True):
                        return {"success": False, "error": "No leaf detected. Please point the camera at a plant leaf."}
                        
                    return {
                        "success": True,
                        "disease": data.get("disease", "Unknown"),
                        "confidence": data.get("confidence", 95),
                        "description": data.get("description", "Analyzed by AI."),
                        "treatment": data.get("treatment", "Consult an agronomist."),
                        "prevention": data.get("prevention", "Maintain plant health.")
                    }
                except Exception as e:
                    print(f"Gemini API Error: {e}")
                    return {"success": False, "error": f"AI service error. {e}"}
            
            # Fallback if no API key
            return {"success": False, "error": "AI Model not configured. Please add GEMINI_API_KEY to crop_project/.env"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

detector = DiseaseDetector()
