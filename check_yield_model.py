import joblib  # type: ignore
import os
import numpy as np  # type: ignore

# Mocking settings for standalone script
BASE_DIR = r'c:\Users\acer\Desktop\CropYieldProject\crop_project'
model_path = os.path.join(BASE_DIR, "yield_model.pkl")  # ✅ Correct: yield model

try:
    model = joblib.load(model_path)
    print(f"Model loaded: {type(model)}")
    if hasattr(model, 'n_features_in_'):
        print(f"n_features_in_: {model.n_features_in_}")
    elif hasattr(model, 'feature_names_in_'):
        print(f"feature_names_in_: {model.feature_names_in_}")
    else:
        # Try a dummy predict to see error
        try:
            model.predict(np.array([[0,0,0]]))
        except Exception as e:
            print(f"Predict error (likely feature mismatch): {e}")
except Exception as e:
    print(f"Load error: {e}")
