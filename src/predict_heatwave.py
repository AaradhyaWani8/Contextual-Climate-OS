import pandas as pd
import pickle
from pathlib import Path

print("\n====================================")
print("     HEATWAVE INTELLIGENCE")
print("       PREDICTION SYSTEM")
print("====================================")

# Load trained model
with open("models/heatwave_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/features.pkl", "rb") as f:
    features = pickle.load(f)

# Load weather dataset for location information
df = pd.read_csv("data/processed/weather_clean.csv")

# Create consistent category mappings
stations = sorted(df["station"].unique())
seasons = sorted(df["season"].unique())

station_codes = {
    name: i for i, name in enumerate(stations)
}

season_codes = {
    name: i for i, name in enumerate(seasons)
}

# Location coordinates
locations = (
    df.groupby("station")[["latitude", "longitude"]]
    .first()
    .to_dict("index")
)

labels = {
    0: "NORMAL",
    1: "HEAT ALERT",
    2: "SEVERE HEAT ALERT"
}

print("\nAvailable Cities:")
for city in stations:
    print("-", city)

city = input("\nEnter city: ").strip().title()

if city not in stations:
    print("Invalid city selected!")
    raise SystemExit

temperature = float(input("Enter maximum temperature (C): "))
humidity = float(input("Enter humidity (%): "))

print("\nAvailable Seasons:")
for season in seasons:
    print("-", season)

season = input("\nEnter season: ").strip().title()

if season not in seasons:
    print("Invalid season selected!")
    raise SystemExit

if not 0 <= humidity <= 100:
    print("Humidity must be between 0 and 100.")
    raise SystemExit

if not -20 <= temperature <= 60:
    print("Temperature must be between -20 and 60.")
    raise SystemExit

# Prepare input
location = locations[city]

input_data = pd.DataFrame([{
    "maximum_temperature": temperature,
    "humidity": humidity,
    "latitude": location["latitude"],
    "longitude": location["longitude"],
    "station_code": station_codes[city],
    "season_code": season_codes[season]
}])[features]

# Predict
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)[0]

confidence = max(probabilities) * 100

print("\n====================================")
print("       PREDICTION RESULTS")
print("====================================")

print("City:", city)
print("Temperature:", temperature, "C")
print("Humidity:", humidity, "%")
print("Season:", season)

print("\nPredicted Heatwave Status:")
print(">>>", labels[prediction])

print(f"\nModel Confidence: {confidence:.2f}%")

print("\nClass Probabilities:")

for i, probability in enumerate(probabilities):
    print(f"{labels[i]}: {probability * 100:.2f}%")

print("\n====================================")
print("  END OF PREDICTION SIMULATION")
print("====================================")

# Save prediction
Path("outputs").mkdir(exist_ok=True)

result = pd.DataFrame([{
    "city": city,
    "temperature": temperature,
    "humidity": humidity,
    "season": season,
    "predicted_status": labels[prediction],
    "confidence": confidence
}])

output_file = Path("outputs/predictions.csv")

if output_file.exists():
    result.to_csv(
        output_file,
        mode="a",
        header=False,
        index=False
    )
else:
    result.to_csv(output_file, index=False)

print("\nPrediction saved to:", output_file)
