from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load model and preprocessing tools
model = joblib.load("obesity_model_optimized.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define the expected feature order (must match training)
expected_feature_order = [
    "Gender", "Age", "Height", "Weight", "family_history", "FAVC", "FCVC", "NCP",
    "CAEC", "SMOKE", "CH2O", "SCC", "FAF", "TUE", "CALC", "MTRANS"
]

# Feature type separation
categorical_cols = ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"]
numerical_cols = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_features = data.get("features", {})

    logging.info("===== Incoming Request =====")
    logging.info("Raw Input Data: %s", user_features)

    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([user_features])

        # Encode categorical features
        for col in categorical_cols:
            if col in input_data:
                try:
                    input_data[col] = label_encoders[col].transform(input_data[col])
                except ValueError:
                    logging.warning(f"Unseen category detected in {col}, replacing with most common value.")
                    input_data[col] = label_encoders[col].transform([label_encoders[col].classes_[0]])[0]
            else:
                raise ValueError(f"Missing required categorical feature: {col}")

        # Convert numerical features
        for col in numerical_cols:
            if col in input_data:
                input_data[col] = input_data[col].astype(float)
            else:
                raise ValueError(f"Missing required numerical feature: {col}")

        # Ensure correct feature order
        input_data = input_data[expected_feature_order]
        logging.info("Final Processed Features (Before Scaling): \n%s", input_data)

        # Apply MinMaxScaler (Same as test.py)
        input_data_scaled = scaler.transform(input_data)

        logging.info("Scaled Features: %s", input_data_scaled)

        # Predict obesity class
        prediction = model.predict(input_data_scaled)
        predicted_label = label_encoders["Obesity"].inverse_transform(prediction)[0]

        logging.info("Raw Prediction: %s", prediction)
        logging.info("Final Predicted Obesity Class: %s", predicted_label)

        return jsonify({"obesity_class": predicted_label})

    except Exception as e:
        logging.error("Error during prediction: %s", str(e))
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
