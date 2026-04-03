import tensorflow as tf
from tensorflow.keras.models import load_model

print("Loading old model...")

model = load_model("soil_model.h5", compile=False)

print("Saving fixed model...")

model.save("soil_model_fixed.h5")

print("Done! New model saved as soil_model_fixed.h5")