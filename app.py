import requests
from flask import Flask, render_template, request, jsonify
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# External API URLs
MODEL_API_URL = "http://127.0.0.1:5001/predict"  # ML Model
GENAI_API_URL = "http://127.0.0.1:5001/generate-plan"  # GENAI Diet & Workout

# Function to convert Yes/No responses to 1/0
def yes_no_to_int(value):
    return 1 if value and value.lower() == "yes" else 0

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Collect user data from form
            user_data = {
                "Gender": request.form.get("gender"),
                "Age": int(request.form.get("age", 0)),
                "Height": float(request.form.get("height", 0.0)),
                "Weight": float(request.form.get("weight", 0.0)),
                "family_history": yes_no_to_int(request.form.get("family_history")),
                "FAVC": yes_no_to_int(request.form.get("favc")),
                "FCVC": float(request.form.get("fcvc", 0)),
                "NCP": float(request.form.get("ncp", 0)),
                "CAEC": request.form.get("caec"),
                "SMOKE": yes_no_to_int(request.form.get("smoke")),
                "CH2O": float(request.form.get("ch2o", 0)),
                "SCC": yes_no_to_int(request.form.get("scc")),
                "FAF": float(request.form.get("faf", 0)),
                "TUE": float(request.form.get("tue", 0)),
                "CALC": request.form.get("calc"),
                "MTRANS": request.form.get("mtrans"),
            }

            print("\n🔹 Received User Data:", json.dumps(user_data, indent=4))  # Debugging

            # Send data to ML model
            model_response = requests.post(MODEL_API_URL, json={"features": user_data})
            if model_response.status_code != 200:
                return render_template("error.html", message="ML Model Error")

            obesity_prediction = model_response.json().get("obesity_class", "Unknown")
            user_data["obesity_class"] = obesity_prediction
            print(f"🔹 Predicted Obesity Class: {obesity_prediction}")

            # Send data to GENAI API for diet & workout
            genai_response = requests.post(GENAI_API_URL, json={
                "user_features": user_data,
                "obesity_class": obesity_prediction
            })

            if genai_response.status_code != 200:
                return render_template("error.html", message="GENAI API Error")
            

            plan = genai_response.json()
            print("\n🔹 Generated Plan:", json.dumps(plan, indent=4))  # Debugging

            # Extracting diet and workout plans properly
            diet_plan = plan.get("diet", {})
            workout_plan = plan.get("workout", {})

            return render_template("result.html", data=user_data, diet=diet_plan, workout=workout_plan)

        except Exception as e:
            return render_template("error.html", message=str(e))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
