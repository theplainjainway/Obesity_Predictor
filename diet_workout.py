import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Set Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_diet_workout(user_data, obesity_level):
    """
    Generates a structured diet and workout plan using Gemini AI.
    """
    prompt = f"""
    The user has the following details:
    - Age: {user_data['Age']}
    - Gender: {user_data['Gender']}
    - Height: {user_data['Height']}m
    - Weight: {user_data['Weight']}kg
    - Activity Level: {user_data['FAF']} (0=none, 1=low, 2=moderate, 3=high)
    - Eating Habits: {user_data['CAEC']} (frequency of eating between meals)
    - Predicted Obesity Level: {obesity_level}

    Based on this, provide the following details in structured JSON format:
    {{
        "diet": "Provide a personalized diet plan with meal recommendations (breakfast, lunch, dinner, snacks).",
        "workout": "Provide a custom workout plan (gym/home exercises with duration)."
    }}
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        if not response.text:
            return {"error": "AI response was empty."}
        
        # Clean AI response
        raw_response = response.text.strip()

        # Remove Markdown code block formatting
        cleaned_response = re.sub(r"^```json|```$", "", raw_response).strip()

        # Parse JSON
        try:
            structured_response = json.loads(cleaned_response)  # Ensure the response is valid JSON
        except json.JSONDecodeError:
            return {"error": "AI response was not in expected JSON format."}

        return {
            "diet": structured_response.get("diet", "No diet plan available."),
            "workout": structured_response.get("workout", "No workout plan available.")
        }

    except Exception as e:
        return {"error": f"Failed to generate AI response: {str(e)}"}

# Example Test
if __name__ == "__main__":
    sample_user = {
        "Age": 25,
        "Gender": "Male",
        "Height": 1.75,
        "Weight": 85,
        "FAF": 1,
        "CAEC": "Sometimes"
    }
    sample_obesity_level = "Overweight"
    plan = generate_diet_workout(sample_user, sample_obesity_level)
    print(plan)
