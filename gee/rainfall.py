"""
rainfall Module
Extracts monthly rainfall (2021–2025) for North America
Computes continental mean and exports to CSV
"""
import ee
from continent_geometry import get_north_america

print("Initializing Earth Engine...")
ee.Initialize(project="gee-climate-dashboard-487203")
print("Earth Engine initialized successfully.")

region = get_north_america()

print("Loading CHIRPS rainfall dataset...")

collection = (ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
              .filterBounds(region)
              .filterDate("2021-01-01", "2025-12-31"))


def monthly_total(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    monthly = collection.filterDate(start, end).sum()

    stats = monthly.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=50000,
        maxPixels=1e13
    )

    return ee.Feature(None, {
        'year': year,
        'month': month,
        'rainfall_mm': stats.get('precipitation')
    })


years = ee.List.sequence(2021, 2025)
months = ee.List.sequence(1, 12)

features = years.map(
    lambda y: months.map(
        lambda m: monthly_total(y, m)
    )
).flatten()

fc = ee.FeatureCollection(features)

print("Starting rainfall export task...")

task = ee.batch.Export.table.toDrive(
    collection=fc,
    description='Rainfall_Monthly_North_America',
    folder='GEE_Exports',
    fileNamePrefix='rainfall_monthly_2021_2025',
    fileFormat='CSV'
)

task.start()

print("Export task started.")
print("Go to Earth Engine Tasks page and click RUN.")
