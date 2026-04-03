import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.ensemble import BaggingRegressor # type: ignore
import joblib # type: ignore
import os

# Path to user's dataset
csv_path = r"c:\Users\acer\Downloads\ML16\final_year _project_detail\CROP.csv"

if os.path.exists(csv_path):
    print(f"Loading user dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # We need to simulate 'Yield' because the original dataset is for classification.
    # Yield formula based on agricultural logic:
    # 1. Base yield (Tons/Hectare)
    # 2. Nutrient bonuses (N, P, K)
    # 3. Environmental penalties (Temp/Rainfall extremes)
    
    def calculate_yield(row):
        # Base yield 3.0 Tons/Hectare
        y = 3.0
        
        # Nutrient impact (assuming 0-140 range for NPK)
        y += (row['N'] / 100.0) * 0.5   # Nitrogen boost
        y += (row['P'] / 100.0) * 0.3   # Phosphorus boost
        y += (row['K'] / 100.0) * 0.2   # Potassium boost
        
        # rainfall impact (optimum around 100-200)
        if row['rainfall'] < 50: y -= 1.0
        elif row['rainfall'] > 250: y -= 0.5
        
        # pH impact (optimum 6-7)
        if abs(row['ph'] - 6.5) > 1.5: y -= 0.6
        
        # Add some randomness for realism
        y += np.random.normal(0, 0.2)
        
        return max(0.5, float(round(float(y), 2))) # type: ignore

    df['Yield_Per_Hectare'] = df.apply(calculate_yield, axis=1)
    
    # Add synthetic 'Area' feature (1.0 to 10.0 hectares)
    df['Area'] = np.random.uniform(1.0, 10.0, size=len(df))
    
    # Total Yield = Area * Yield_Per_Hectare
    df['Total_Yield'] = df['Area'] * df['Yield_Per_Hectare']
    
    # Features for the model: N, P, K, temperature, humidity, ph, rainfall, Area
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'Area']]
    y = df['Total_Yield']
    
    print(f"Training on {len(df)} samples with 8 features...")
    
    model = BaggingRegressor(n_estimators=20, random_state=42)
    model.fit(X, y)
    
    # Save the model
    save_path = "yield_model.pkl"
    joblib.dump(model, save_path)
    
    print(f"Enhanced yield_model.pkl created with 8 features!")
    print(f"Mean Yield in dataset: {y.mean():.2f} Tons")

else:
    print("User dataset not found! Falling back to synthetic training.")
    # Fallback to a smaller synthetic set if CSV is missing
    data = {
        "N": [90, 80, 70, 60, 50, 40],
        "P": [40, 45, 50, 55, 60, 65],
        "K": [40, 35, 30, 25, 20, 15],
        "temperature": [25, 28, 30, 32, 22, 20],
        "humidity": [80, 75, 70, 65, 85, 90],
        "ph": [6.5, 6.0, 7.0, 5.5, 7.5, 6.2],
        "rainfall": [200, 150, 100, 80, 250, 300],
        "Area": [2.0, 3.0, 4.0, 5.0, 1.5, 1.0],
        "Yield": [10.2, 12.5, 15.0, 18.2, 5.5, 4.0]
    }
    df = pd.DataFrame(data)
    X = df.drop("Yield", axis=1)
    y = df["Yield"]
    model = BaggingRegressor(n_estimators=10, random_state=42)
    model.fit(X, y)
    joblib.dump(model, "yield_model.pkl")
    print("Synthetic yield_model.pkl created.")