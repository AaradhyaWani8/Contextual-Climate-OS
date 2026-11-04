import numpy as np
import pandas as pd
from pathlib import Path

# Reproducible synthetic weather simulation
np.random.seed(42)

# Seven representative Indian weather stations
stations = [
    {"city": "Delhi", "state": "Delhi",
     "lat": 28.6139, "lon": 77.2090, "base": 30, "amplitude": 9},

    {"city": "Jaipur", "state": "Rajasthan",
     "lat": 26.9124, "lon": 75.7873, "base": 30, "amplitude": 9},

    {"city": "Ahmedabad", "state": "Gujarat",
     "lat": 23.0225, "lon": 72.5714, "base": 31, "amplitude": 8},

    {"city": "Mumbai", "state": "Maharashtra",
     "lat": 19.0760, "lon": 72.8777, "base": 30, "amplitude": 4},

    {"city": "Pune", "state": "Maharashtra",
     "lat": 18.5204, "lon": 73.8567, "base": 28, "amplitude": 6},

    {"city": "Nagpur", "state": "Maharashtra",
     "lat": 21.1458, "lon": 79.0882, "base": 30, "amplitude": 8},

    {"city": "Chennai", "state": "Tamil Nadu",
     "lat": 13.0827, "lon": 80.2707, "base": 30, "amplitude": 4}
]

dates = pd.date_range(
    start="2023-01-01",
    end="2025-12-31",
    freq="D"
)

records = []

for station in stations:

    for date in dates:

        day = date.day_of_year

        # Annual temperature variation
        seasonal_temp = station["base"] + station["amplitude"] * np.sin(
            2 * np.pi * (day - 45) / 365
        )

        # Additional temperature variation
        noise = np.random.normal(0, 1.8)

        # Simulated maximum temperature
        max_temp = seasonal_temp + noise

        # Additional synthetic heatwave-like conditions
        if date.month in [3, 4, 5] and station["city"] not in [
            "Mumbai", "Chennai"
        ]:
            if np.random.random() < 0.12:
                max_temp += np.random.uniform(2, 5)

        # Simulated humidity
        humidity = np.random.uniform(25, 90)

        # Four seasonal categories
        if date.month in [12, 1, 2]:
            season = "Winter"
        elif date.month in [3, 4, 5]:
            season = "Pre-Monsoon"
        elif date.month in [6, 7, 8, 9]:
            season = "Monsoon"
        else:
            season = "Post-Monsoon"

        records.append({
            "timestamp": date,
            "station": station["city"],
            "state": station["state"],
            "latitude": station["lat"],
            "longitude": station["lon"],
            "maximum_temperature": round(max_temp, 2),
            "humidity": round(humidity, 2),
            "season": season,
            "source_type": "SYNTHETIC"
        })

# Convert observations into a DataFrame
df = pd.DataFrame(records)

# Save the dataset
output_path = Path("data/raw/weather_data.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("\n====================================")
print(" HEATWAVE INTELLIGENCE")
print(" WEATHER DATA SIMULATION")
print("====================================")

print(f"\nTotal observations: {len(df)}")
print(f"Number of stations: {df['station'].nunique()}")

print("\nStation-wise observations:")
print(df.groupby("station").size())

print("\nSample weather observations:")
print(df.head(10).to_string(index=False))

print(f"\nDataset saved successfully: {output_path}")
print("\nNOTE: This is synthetic demonstration data.")
print("It is NOT actual IMD weather data.")
