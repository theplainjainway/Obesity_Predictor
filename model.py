from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import logging
import os
from dotenv import load_dotenv
from diet_workout import generate_diet_workout


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load model and preprocessing tools
model = joblib.load("obesity_model_optimized.pkl")
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

        # Predict obesity class
        prediction = model.predict(input_data)
        predicted_label = label_encoders["Obesity"].inverse_transform(prediction)[0]

        logging.info("Raw Prediction: %s", prediction)
        logging.info("Final Predicted Obesity Class: %s", predicted_label)

        return jsonify({"obesity_class": predicted_label})

    except Exception as e:
        logging.error("Error during prediction: %s", str(e))
        return jsonify({"error": str(e)})

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json
    obesity_class = data.get("obesity_class")
    user_features = data.get("user_features", {})

    if not obesity_class or not user_features:
        return jsonify({"error": "Obesity class and user features are required"}), 400

    try:
        plan = generate_diet_workout(user_features, obesity_class)
        return jsonify(plan)

    except Exception as e:
        logging.error(f"Error generating plan: {str(e)}")
        return jsonify({"error": "Failed to generate a plan"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
