from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model and preprocessing tools
model = joblib.load("obesity_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)

    # Scale features
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    
    return jsonify({"obesity_class": int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
