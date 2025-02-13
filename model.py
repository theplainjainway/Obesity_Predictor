from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model and preprocessing tools
model = joblib.load("obesity_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")  # Load label encoders for categorical features

# Define expected feature columns
categorical_cols = ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"]
numerical_cols = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]  # Ensure correct list

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_features = data["features"]

    try:
        processed_features = []
        
        # Encode categorical features
        for col in categorical_cols:
            if user_features[col] in label_encoders[col].classes_:
                encoded_value = label_encoders[col].transform([user_features[col]])[0]
            else:
                encoded_value = label_encoders[col].transform([label_encoders[col].classes_[0]])[0]  # Default to first class
            processed_features.append(encoded_value)
        
        # Append numerical features directly
        for col in numerical_cols:
            processed_features.append(float(user_features[col]))  # Ensure float type
        
        # Convert to NumPy array and scale
        features = np.array(processed_features).reshape(1, -1)
        scaled_features = scaler.transform(features)  # Ensure correct feature count
        
        # Predict obesity class
        prediction = model.predict(scaled_features)
        
        return jsonify({"obesity_class": int(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
