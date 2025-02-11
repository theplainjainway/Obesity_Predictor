import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
file_path = "Obesity prediction.csv"
df = pd.read_csv(file_path)

# Exploratory Data Analysis (EDA)
# Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap")
#plt.show()

# Histograms for numerical variables
df.select_dtypes(include=['float64']).hist(figsize=(15, 12), bins=20, edgecolor='black', grid=False)
plt.suptitle("Feature Distributions", fontsize=16)
#plt.show()

# Countplot for categorical variables
categorical_cols = ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS", "Obesity"]
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

for i, col in enumerate(categorical_cols):
    sns.countplot(x=df[col], ax=axes[i], palette="Set2")
    axes[i].set_title(f"Distribution of {col}")
    axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=30)

plt.tight_layout()
#plt.show()

# Encode categorical variables
label_encoders = {}
categorical_cols = ["Gender", "family_history", "FAVC", "CAEC", "SMOKE", "SCC", "CALC", "MTRANS", "Obesity"]
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split features and target
X = df.drop(columns=["Obesity"])
y = df["Obesity"]

# Normalize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save the model and scaler
joblib.dump(clf, "obesity_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Predictions and evaluation
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Flask API setup
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    
    # Load model and scaler
    model = joblib.load("obesity_model.pkl")
    scaler = joblib.load("scaler.pkl")
    
    # Scale features
    scaled_features = scaler.transform(features)
    prediction = model.predict(scaled_features)
    
    return jsonify({"obesity_class": int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
