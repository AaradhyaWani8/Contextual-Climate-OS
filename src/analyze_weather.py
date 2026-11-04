import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("\n====================================")
print("    HEATWAVE INTELLIGENCE")
print("     WEATHER DATA ANALYSIS")
print("====================================")

# Load dataset
df = pd.read_csv("data/processed/weather_clean.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Output directory
output_dir = Path("outputs/graphs")
output_dir.mkdir(parents=True, exist_ok=True)

# Heatwave categories
def classify(temp):
    if temp >= 40:
        return "Severe Heat Alert"
    elif temp >= 35:
        return "Heat Alert"
    return "Normal"

df["heatwave_status"] = df[
    "maximum_temperature"
].apply(classify)

# 1. City-wise temperature comparison
print("\n1. City-wise average temperature")

city_avg = df.groupby("station")[
    "maximum_temperature"
].mean().sort_values(ascending=False)

print(city_avg.round(2))

plt.figure(figsize=(10, 6))
city_avg.plot(kind="bar")
plt.title("Average Temperature by City")
plt.xlabel("Weather Station")
plt.ylabel("Temperature (C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "city_temperature.png")
plt.close()

# 2. Monthly temperature trend
print("\n2. Monthly temperature trend")

df["month"] = df["timestamp"].dt.month

monthly = df.groupby("month")[
    "maximum_temperature"
].mean()

print(monthly.round(2))

plt.figure(figsize=(10, 6))
monthly.plot(marker="o")
plt.title("Monthly Average Temperature Trend")
plt.xlabel("Month")
plt.ylabel("Temperature (C)")
plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.savefig(output_dir / "monthly_trend.png")
plt.close()

# 3. Heatwave severity distribution
print("\n3. Heatwave category distribution")

distribution = df["heatwave_status"].value_counts()

print(distribution)

plt.figure(figsize=(8, 6))
distribution.plot(kind="bar")
plt.title("Heatwave Severity Distribution")
plt.xlabel("Category")
plt.ylabel("Number of Observations")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(output_dir / "heatwave_distribution.png")
plt.close()

# 4. Temperature and humidity relationship
print("\n4. Temperature vs Humidity")

plt.figure(figsize=(9, 6))
plt.scatter(
    df["humidity"],
    df["maximum_temperature"],
    alpha=0.3
)
plt.title("Temperature vs Humidity")
plt.xlabel("Humidity (%)")
plt.ylabel("Maximum Temperature (C)")
plt.tight_layout()
plt.savefig(output_dir / "temperature_humidity.png")
plt.close()

# Save city summary
city_avg.to_csv(
    "outputs/city_temperature_summary.csv"
)

print("\n====================================")
print(" WEATHER ANALYSIS COMPLETED")
print("====================================")

print("\nGraphs saved in:", output_dir)
print("City summary saved successfully!")
