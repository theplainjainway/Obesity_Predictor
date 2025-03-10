import joblib
import numpy as np
import pandas as pd
import requests

# Load trained components
model = joblib.load("obesity_model_optimized.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# New user input (modify as needed)
input_data = pd.DataFrame([{
    "Gender": "Female",
    "Age": 21,
    "Height": 1.72,
    "Weight": 80,
    "family_history": "yes",
    "FAVC": "yes",
    "FCVC": 2,
    "NCP": 3,
    "CAEC": "Frequently",
    "SMOKE": "no",
    "CH2O": 2,
    "SCC": "yes",
    "FAF": 2,
    "TUE": 1,
    "CALC": "Sometimes",
    "MTRANS": "Public_Transportation"
}])

# Encode categorical variables
for feature in ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"]:
    input_data[feature] = label_encoders[feature].transform(input_data[feature])

# Scale numerical values
input_data_scaled = scaler.transform(input_data)

# Make prediction
prediction = model.predict(input_data_scaled)
predicted_label = label_encoders["Obesity"].inverse_transform(prediction)[0]

print("Predicted Obesity Level:", predicted_label)

# ✅ Convert DataFrame to a JSON-friendly format
input_data_dict = input_data.to_dict(orient="records")[0]  # Convert DataFrame row to dictionary

# Send the predicted obesity level to the GenAI API
api_url = "http://127.0.0.1:5001/generate-plan"  # Update if your Flask API is hosted elsewhere
payload = {
    "obesity_class": predicted_label,  # Send the actual predicted class
    "user_features": input_data_dict  # JSON-friendly user features
}

try:
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        result = response.json()
        print("\n🔹 Personalized Diet & Workout Plan 🔹")
        print("Diet Plan:", result.get("diet_plan", "No plan available"))
        print("Workout Plan:", result.get("workout_plan", "No plan available"))
    else:
        print("Error:", response.text)
except requests.exceptions.RequestException as e:
    print("Failed to connect to the GenAI API:", e)
