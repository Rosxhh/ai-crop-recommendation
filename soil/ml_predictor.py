"""
soil/ml_predictor.py
────────────────────
Loads the locally-trained soil CNN (soil_model.h5) that was trained on
~6000 images across 6 Indian soil categories and exposes a single
predict_soil_type() helper used by both soil/views.py and analysis/views.py.

Model classes (alphabetical – must match the folder order used during training):
    0: Alluvial_Soil
    1: Arid_Soil
    2: Laterite_Soil
    3: Mountain_Soil
    4: Red_Soil
    5: Yellow_Soil

Mapping to app soil types (Sandy / Clay / Loamy / Silty / Peaty / Chalky):
    Alluvial  → Loamy   (Indo-Gangetic plains, highly fertile, silty-loamy)
    Arid      → Sandy   (Rajasthan desert soils, sandy, low moisture)
    Laterite  → Clay    (Western Ghats, iron-rich, clay-heavy)
    Mountain  → Silty   (Himalayan young soils, mineral-rich silty texture)
    Red       → Chalky  (Deccan plateau, iron oxide, well-drained, alkaline)
    Yellow    → Peaty   (Organic-rich, slightly acidic, found near water bodies)

Usage:
    from soil.ml_predictor import predict_soil_type
    soil_name, raw_class, confidence = predict_soil_type(pil_img)
    # soil_name → e.g. "Loamy"  (or None if model unavailable)
    # raw_class → e.g. "Alluvial_Soil"
    # confidence → e.g. 87.3  (percentage)
"""

import os
import numpy as np

# ──────────────────────────────────────────────────────────
# Class order MUST match the alphabetical folder names that
# Keras assigns during image_dataset_from_directory()
# ──────────────────────────────────────────────────────────
MODEL_CLASSES = [
    "Alluvial_Soil",
    "Arid_Soil",
    "Laterite_Soil",
    "Mountain_Soil",
    "Red_Soil",
    "Yellow_Soil",
]

# Map from model's Indian soil category → app's international soil type
SOIL_CATEGORY_MAP = {
    "Alluvial_Soil":  "Loamy",
    "Arid_Soil":      "Sandy",
    "Laterite_Soil":  "Clay",
    "Mountain_Soil":  "Silty",
    "Red_Soil":       "Chalky",
    "Yellow_Soil":    "Peaty",
}

# Friendly display names for Indian soil types (shown alongside the mapped type)
INDIAN_SOIL_DISPLAY = {
    "Alluvial_Soil":  "Alluvial Soil",
    "Arid_Soil":      "Arid / Desert Soil",
    "Laterite_Soil":  "Laterite Soil",
    "Mountain_Soil":  "Mountain / Forest Soil",
    "Red_Soil":       "Red Soil",
    "Yellow_Soil":    "Yellow Soil",
}

# Singleton model cache (loaded once on first call)
_soil_model = None
_model_load_attempted = False


def _load_model():
    """Load soil_model.h5 once and cache it. Returns None if unavailable."""
    global _soil_model, _model_load_attempted
    if _model_load_attempted:
        return _soil_model

    _model_load_attempted = True
    try:
        from django.conf import settings          # type: ignore
        from tensorflow.keras.models import load_model  # type: ignore
        model_path = os.path.join(settings.BASE_DIR, "soil_model.h5")
        if not os.path.exists(model_path):
            print("[SoilML] soil_model.h5 not found – local prediction disabled.")
            return None
        _soil_model = load_model(model_path, compile=False)
        print(f"[SoilML] ✅ soil_model.h5 loaded successfully ({model_path})")
    except Exception as e:
        print(f"[SoilML] ⚠️  Failed to load soil_model.h5: {e}")
        _soil_model = None
    return _soil_model


def predict_soil_type(pil_image):
    """
    Classify a PIL Image using the locally trained soil CNN.

    Parameters
    ----------
    pil_image : PIL.Image.Image
        Any size / mode – will be converted to RGB 128×128 internally.

    Returns
    -------
    tuple: (app_soil_type, raw_class, indian_display_name, confidence_pct)
        app_soil_type     : str  – one of Sandy/Clay/Loamy/Silty/Peaty/Chalky
        raw_class         : str  – e.g. "Alluvial_Soil"
        indian_display    : str  – e.g. "Alluvial Soil"
        confidence_pct    : float – 0-100

    Returns (None, None, None, 0.0) if prediction is not possible.
    """
    model = _load_model()
    if model is None:
        return None, None, None, 0.0

    try:
        # ── Pre-processing ──────────────────────────────────────────────
        # Model has Rescaling(1./255) as its FIRST layer, so we pass
        # raw uint8 pixel values (0-255) – do NOT divide manually.
        img = pil_image.convert("RGB")
        img = img.resize((128, 128))               # exact training size
        img_array = np.array(img, dtype=np.float32)  # raw 0-255 values
        img_array = np.expand_dims(img_array, axis=0)  # shape (1, 128, 128, 3)

        # ── Inference ───────────────────────────────────────────────────
        preds = model.predict(img_array, verbose=0)  # shape (1, 6)
        predicted_idx = int(np.argmax(preds[0]))
        confidence = float(preds[0][predicted_idx]) * 100.0

        raw_class = MODEL_CLASSES[predicted_idx]
        app_soil_type = SOIL_CATEGORY_MAP.get(raw_class, "Loamy")
        indian_display = INDIAN_SOIL_DISPLAY.get(raw_class, raw_class)

        return app_soil_type, raw_class, indian_display, confidence

    except Exception as e:
        print(f"[SoilML] Prediction error: {e}")
        return None, None, None, 0.0
