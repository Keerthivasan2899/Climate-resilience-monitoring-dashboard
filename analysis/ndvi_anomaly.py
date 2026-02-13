import pandas as pd

print("Loading NDVI data from CSV...")

df = pd.read_csv("data/ndvi_monthly_2021_2025.csv")

# keep only relevant columns
df = df[["year", "month", "ndvi"]]

# Ensure correct data types
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["ndvi"] = pd.to_numeric(df["ndvi"], errors="coerce")
print("NDVI data loaded successfully.")

# Calculate monthly anomalies
print("Calculating 5 year monthly baseline...")

monthly_baseline = df.groupby("month")["ndvi"].mean().reset_index()
monthly_baseline.rename(columns={"ndvi": "baseline_ndvi"}, inplace=True)

df = df.merge(monthly_baseline, on="month")

df["anomaly"] = df["ndvi"] - df["baseline_ndvi"]

print("Saving cleaned anomaly data to CSV...")
df.to_csv("data/ndvi_with_anomaly.csv", index=False)

print("NDVI anomaly data calculation saved successfully.")
