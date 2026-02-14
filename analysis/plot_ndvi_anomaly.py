import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data (REMOVED the leading slash)
df = pd.read_csv("data/ndvi_with_anomaly.csv")

# 2. Create the 'date' column from year and month
# This is necessary because the CSV only has separate year/month columns
df["date"] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# 3. Sort by date to ensure the line graph flows correctly
df = df.sort_values("date")

# 4. Create figure
plt.figure(figsize=(12, 6))

# 5. Plot anomaly (FIXED column name to 'anomaly')
# We use a color logic: Red for negative (stress), Green for positive (healthy)
plt.bar(df["date"], df["anomaly"], width=20,
        color=['red' if x < 0 else 'green' for x in df["anomaly"]])

# 6. Title and labels
plt.title("NDVI Monthly Anomaly (North America, 2021–2025)", fontsize=14)
plt.xlabel("Timeline", fontsize=12)
plt.ylabel("Health Deviation (Anomaly)", fontsize=12)
plt.axhline(0, color='black', linewidth=0.8)  # Adds a center line at zero

# 7. Improve layout
plt.xticks(rotation=45)
plt.tight_layout()

# 8. Save as high resolution PNG
plt.savefig("ndvi_anomaly_plot.png", dpi=300)
print("Graph saved successfully as ndvi_anomaly_plot.png")

plt.show()
