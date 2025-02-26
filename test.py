import joblib
import numpy as np
import pandas as pd

# Load trained components
model = joblib.load("obesity_model_optimized.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# New user input (as per your example)
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
predicted_label = label_encoders["Obesity"].inverse_transform(prediction)

print("Predicted Obesity Level:", predicted_label[0])

# Load the saved label encoders
label_encoders = joblib.load("label_encoders.pkl")

# Print mappings for all categorical features
for feature, encoder in label_encoders.items():
    mapping = {index: category for index, category in enumerate(encoder.classes_)}
    print(f"{feature} Encoding Mapping: {mapping}\n")

# Load dataset
file_path = "Obesity prediction.csv"
df = pd.read_csv(file_path)

# Print unique values in ascending order
print("FCVC Unique Values:", sorted(df["FCVC"].unique()))
print("NCP Unique Values:", sorted(df["NCP"].unique()))
print("FAF Unique Values:", sorted(df["FAF"].unique()))

