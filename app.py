import requests
from flask import Flask, render_template, request

app = Flask(__name__)

MODEL_API_URL = "http://127.0.0.1:5001/predict"  # Ensure model.py runs on a different port

# Function to convert Yes/No responses to 1/0
def yes_no_to_int(value):
    return 1 if value.lower() == "yes" else 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = {
            'gender': yes_no_to_int(request.form['gender']),
            'age': request.form['age'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'family_history': yes_no_to_int(request.form['family_history']),
            'favc': yes_no_to_int(request.form['favc']),
            'fcvc': request.form['fcvc'],
            'ncp': request.form['ncp'],
            'caec': yes_no_to_int(request.form['caec']),
            'smoke': yes_no_to_int(request.form['smoke']),
            'ch2o': request.form['ch2o'],
            'scc': yes_no_to_int(request.form['scc']),
            'faf': request.form['faf'],
            'tue': request.form['tue'],
            'calc': request.form['calc'],
            'mtrans': request.form['mtrans'],
        }

        # Send request to model.py
        response = requests.post(MODEL_API_URL, json={"features": list(user_data.values())})
        
        if response.status_code == 200:
            prediction = response.json().get("obesity_class", "Unknown")
            user_data['obesity_class'] = prediction

        return render_template('result.html', data=user_data)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
