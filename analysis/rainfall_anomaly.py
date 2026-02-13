import pandas as pd

print("Loading rainfall CSV...")

df = pd.read_csv("data/rainfall_monthly_2021_2025.csv")

# Keep only required columns
df = df[["year", "month", "rainfall_mm"]]

# Ensure correct data types
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")

print("Computing 5-year monthly rainfall baseline...")

monthly_baseline = df.groupby("month")["rainfall_mm"].mean().reset_index()
monthly_baseline.rename(
    columns={"rainfall_mm": "baseline_rainfall"}, inplace=True)

df = df.merge(monthly_baseline, on="month")

df["anomaly"] = df["rainfall_mm"] - df["baseline_rainfall"]

print("Saving rainfall anomaly CSV...")

df.to_csv("data/rainfall_with_anomaly.csv", index=False)

print("Rainfall anomaly calculation completed successfully.")
