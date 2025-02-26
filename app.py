import requests
from flask import Flask, render_template, request # type: ignore
import json

app = Flask(__name__)

MODEL_API_URL = "http://127.0.0.1:5001/predict"  # Ensure model.py runs on a different port

# Function to convert Yes/No responses to 1/0
def yes_no_to_int(value):
    return 1 if value.lower() == "yes" else 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'Gender': request.form.get('gender'),
            'Age': int(request.form.get('age', 0)),
            'Height': float(request.form.get('height', 0.0)),
            'Weight': float(request.form.get('weight', 0.0)),
            'family_history': request.form.get('family_history'),
            'FAVC': request.form.get('favc'),
            'FCVC': float(request.form.get('fcvc', 0)),
            'NCP': float(request.form.get('ncp', 0)),
            'CAEC': request.form.get('caec'),
            'SMOKE': request.form.get('smoke'),
            'CH2O': int(request.form.get('ch2o', 0)),
            'SCC': request.form.get('scc'),
            'FAF': float(request.form.get('faf', 0)),
            'TUE': int(request.form.get('tue', 0)),
            'CALC': request.form.get('calc'),
            'MTRANS': request.form.get('mtrans'),
        }

        print("Received Data:", json.dumps(user_data, indent=4))  # Debugging

        response = requests.post(MODEL_API_URL, json={"features": user_data})
                
        if response.status_code == 200:
            prediction = response.json().get("obesity_class", "Unknown")

            user_data['obesity_class'] = prediction
            print(f"Debug - Predicted Obesity Class: {prediction} ({type(prediction)})")

            return render_template('result.html', data=user_data)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
