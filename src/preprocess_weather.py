import pandas as pd
from pathlib import Path

print("\n====================================")
print(" HEATWAVE INTELLIGENCE")
print(" WEATHER DATA PREPROCESSING")
print("====================================")

# Load raw dataset
input_file = Path("data/raw/weather_data.csv")
output_file = Path("data/processed/weather_clean.csv")

df = pd.read_csv(input_file)

print("\n1. Original dataset information")
print("Total records:", len(df))
print("Total columns:", len(df.columns))

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Convert numeric columns
numeric_columns = [
    "latitude",
    "longitude",
    "maximum_temperature",
    "humidity"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# Check missing values
print("\n2. Missing values before cleaning")
print(df.isnull().sum())

# Remove duplicate records
before = len(df)
df = df.drop_duplicates()
duplicates = before - len(df)

# Remove invalid records
df = df.dropna(
    subset=[
        "timestamp",
        "station",
        "maximum_temperature",
        "latitude",
        "longitude",
        "humidity"
    ]
)

# Validate humidity
df = df[
    (df["humidity"] >= 0) &
    (df["humidity"] <= 100)
]

# Validate geographical coordinates
df = df[
    (df["latitude"].between(-90, 90)) &
    (df["longitude"].between(-180, 180))
]

# Sort records
df = df.sort_values(
    ["station", "timestamp"]
).reset_index(drop=True)

# Save cleaned dataset
output_file.parent.mkdir(
    parents=True, exist_ok=True
)

df.to_csv(output_file, index=False)

print("\n3. Cleaning summary")
print("Duplicate records removed:", duplicates)
print("Final records:", len(df))
print("Missing values remaining:", df.isnull().sum().sum())

print("\n4. Station-wise average temperature")
print(
    df.groupby("station")["maximum_temperature"]
    .mean()
    .round(2)
)

print("\n5. Temperature statistics")
print(
    df["maximum_temperature"].describe().round(2)
)

print("\nCleaned dataset saved at:", output_file)
print("\nPREPROCESSING COMPLETED SUCCESSFULLY!")
