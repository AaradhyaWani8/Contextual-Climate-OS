import pandas as pd
import numpy as np
import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("\n====================================")
print(" HEATWAVE INTELLIGENCE")
print(" AI MODEL TRAINING")
print("====================================")

# Load cleaned data
df = pd.read_csv("data/processed/weather_clean.csv")

# Create heatwave severity labels
def classify_heatwave(temp):
    if temp >= 40:
        return 2
    elif temp >= 35:
        return 1
    else:
        return 0

df["heatwave_level"] = df["maximum_temperature"].apply(
    classify_heatwave
)

# Encode categorical features
df["station_code"] = df["station"].astype("category").cat.codes
df["season_code"] = df["season"].astype("category").cat.codes

# Feature selection
features = [
    "maximum_temperature",
    "humidity",
    "latitude",
    "longitude",
    "station_code",
    "season_code"
]

X = df[features]
y = df["heatwave_level"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42,
    class_weight="balanced"
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n====================================")
print(" MODEL EVALUATION")
print("====================================")

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Normal",
            "Heat Alert",
            "Severe Heat Alert"
        ],
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Save model
Path("models").mkdir(exist_ok=True)

with open("models/heatwave_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save feature information
with open("models/features.pkl", "wb") as file:
    pickle.dump(features, file)

print("\nModel saved: models/heatwave_model.pkl")
print("Features saved: models/features.pkl")

print("\nMODEL TRAINING COMPLETED SUCCESSFULLY!")
