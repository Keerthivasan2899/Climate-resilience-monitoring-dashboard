import pandas as pd

df = pd.read_csv("data/ndvi_monthly_Mexico_2021_2025.csv")

df = df[["year", "month", "ndvi"]]

df["date"] = pd.to_datetime(
    df["year"].astype(int).astype(str) + "-" +
    df["month"].astype(int).astype(str) + "-01"
)

df = df[["date", "ndvi"]]

df.to_csv("data/ndvi_Mexico_clean.csv", index=False)
