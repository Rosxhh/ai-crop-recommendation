import joblib
import numpy as np
import os

BASE_DIR = r'c:\Users\acer\Desktop\CropYieldProject\crop_project'
model_path = os.path.join(BASE_DIR, "yield_model.pkl")
model = joblib.load(model_path)

# Sample data from predictor/views.py defaults
nitrogen = 90
phosphorus = 42
potassium = 43
temperature = 28.5
humidity = 80
ph = 6.5
rainfall = 120.5
area = 10.5

input_data = np.array([[
    nitrogen, 
    phosphorus, 
    potassium, 
    temperature, 
    humidity, 
    ph, 
    rainfall, 
    area
]])

try:
    prediction = model.predict(input_data)
    print(f"Prediction: {prediction}")
    print(f"Prediction[0]: {prediction[0]}")
    total_yield = round(float(prediction[0]), 2)
    print(f"Total Yield: {total_yield}")
except Exception as e:
    print(f"Error during prediction: {e}")
