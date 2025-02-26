import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import RandomOverSampler

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

# Address class imbalance
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestClassifier(class_weight="balanced", random_state=42), param_grid, cv=5)
grid_search.fit(X_train, y_train)

best_clf = grid_search.best_estimator_

# Save the best model, scaler, and label encoders
joblib.dump(best_clf, "obesity_model_optimized.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Predictions and evaluation
y_pred = best_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Feature importance analysis
importances = best_clf.feature_importances_
feature_names = X.columns
plt.figure(figsize=(10, 5))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importance")
#plt.show()

# Check label decoding
decoded_predictions = label_encoders["Obesity"].inverse_transform(y_pred)
print("Decoded Predictions:", decoded_predictions)
