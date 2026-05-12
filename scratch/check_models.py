import joblib
import os

def check_model(path):
    if not os.path.exists(path):
        print(f"File {path} not found.")
        return
    
    try:
        model = joblib.load(path)
        print(f"\n--- Model: {path} ---")
        print(f"Type: {type(model)}")
        
        # Check for feature names (scikit-learn 1.0+)
        if hasattr(model, 'feature_names_in_'):
            print(f"Feature Names In: {model.feature_names_in_}")
        else:
            print("Feature names not found (model might have been fitted with a numpy array).")
            
        # Check if it's a Bagging model and its base estimator
        if hasattr(model, 'base_estimator_'):
            print(f"Base Estimator: {type(model.base_estimator_)}")
            
    except Exception as e:
        print(f"Error loading {path}: {e}")

if __name__ == "__main__":
    check_model("crop1.pkl")
    check_model("yield_model.pkl")
