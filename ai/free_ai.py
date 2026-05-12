import logging

logger = logging.getLogger(__name__)

class DummyResponse:
    def __init__(self, text="This is a free AI response from AgriCore's local model."):
        self.text = text

class DummyModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_content(self, content, **kwargs):
        logger.info(f"FreeAI generating content for model {self.model_name}")
        # If it's a list (like in vision tasks), just ignore the image part for the dummy response
        if isinstance(content, list):
             prompt = str(content)
             if "JSON" in prompt:
                 if "soil" in prompt.lower() or "Sandy" in prompt:
                     # Soil Analysis JSON
                     return DummyResponse(text='{"type": "Loamy", "confidence": 95, "texture": "Fine", "color": "Dark", "moisture": "Moist", "organic_matter": "High", "ph_estimate": 6.5, "regional_name": "Alluvial Soil", "top_crops": ["Rice", "Wheat", "Potato"], "best_practices": ["Maintain organic mulching", "Check pH monthly", "Ensure proper drainage"], "bad_practices": ["Avoid heavy chemical usage", "Do not over-water", "Avoid compacting wet soil"]}')
                 else:
                     # Disease Detection JSON
                     return DummyResponse(text='{"crop": "Plant", "disease": "Healthy Leaf", "confidence": 98.0, "treatment_organic": "Continue balanced organic nutrition.", "treatment_chemical": "None required.", "risk_level": "Low"}')
        return DummyResponse()

def configure(api_key=None, **kwargs):
    logger.info("FreeAI configured (no-op)")
    pass

def list_models():
    class Model:
        def __init__(self, name):
            self.name = name
            self.supported_generation_methods = ['generateContent']
    return [Model('free-agricore-model')]

def GenerativeModel(model_name, **kwargs):
    return DummyModel(model_name)
