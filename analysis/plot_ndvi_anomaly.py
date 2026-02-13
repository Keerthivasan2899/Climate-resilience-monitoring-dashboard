import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../data/ndvi_with_anomaly.csv")

# Ensure date column is datetime
df["date"] = pd.to_datetime(df["date"])

# Sort just in case
df = df.sort_values("date")

# Create figure
plt.figure(figsize=(12, 6))

# Plot anomaly
plt.plot(df["date"], df["ndvi_anomaly"])

# Title and labels
plt.title("NDVI Monthly Anomaly (Americas, 2021–2025)")
plt.xlabel("Date")
plt.ylabel("NDVI Anomaly")

# Improve layout
plt.xticks(rotation=45)
plt.tight_layout()

# Save as high resolution PNG
plt.savefig("ndvi_anomaly_2021_2025.png", dpi=300)

plt.show()
