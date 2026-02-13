import pandas as pd

print("Loading flood CSV...")

df = pd.read_csv("data/flood_monthly_2021_2025.csv")

# Keep only the year, month, and flood area columns
df = df[["year", "month", "flood_area_km2"]]

# Ensure numeric types
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["flood_area_km2"] = pd.to_numeric(df["flood_area_km2"], errors="coerce")

print("Computing 5-year monthly flood baseling...")

monthly_baseline = df.groupby("month")["flood_area_km2"].mean().reset_index()
monthly_baseline.rename(
    columns={"flood_area_km2": "baseline_flood_area"}, inplace=True)

df = df.merge(monthly_baseline, on="month")

df["anomaly"] = df["flood_area_km2"] - df["baseline_flood_area"]

print("Saving flood anomaly CSV...")

df.to_csv("data/flood_with_anomaly.csv", index=False)

print("Flood anomaly calculation completed successfully.")
