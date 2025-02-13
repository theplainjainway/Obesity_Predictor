import requests
from flask import Flask, render_template, request # type: ignore

app = Flask(__name__)

MODEL_API_URL = "http://127.0.0.1:5001/predict"  # Ensure model.py runs on a different port

# Function to convert Yes/No responses to 1/0
def yes_no_to_int(value):
    return 1 if value.lower() == "yes" else 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'Gender': request.form['gender'],
            'Age': request.form['age'],
            'Height': request.form['height'],
            'Weight': request.form['weight'],
            'family_history': request.form['family_history'],
            'FAVC': request.form['favc'],
            'FCVC': request.form['fcvc'],
            'NCP': request.form['ncp'],
            'CAEC': request.form['caec'],
            'SMOKE': request.form['smoke'],
            'CH2O': request.form['ch2o'],
            'SCC': request.form['scc'],
            'FAF': request.form['faf'],
            'TUE': request.form['tue'],
            'CALC': request.form['calc'],
            'MTRANS': request.form['mtrans'],
        }

        # Send request to model.py
        response = requests.post(MODEL_API_URL, json={"features": user_data})  # Fix: send user_data as dictionary
        
        if response.status_code == 200:
            prediction = response.json().get("obesity_class", "Unknown")
            user_data['obesity_class'] = prediction

        return render_template('result.html', data=user_data)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
