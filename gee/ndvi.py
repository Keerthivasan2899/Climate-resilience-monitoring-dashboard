import ee
import pandas as pd
from continent_geometry import get_north_america

print("Initializing Earth Engine...")
ee.Initialize(project="gee-climate-dashboard-487203")
print("Earth Engine initialized successfully.")

print("Getting North America geometry...")
region = get_north_america()

# NDVI function
print("Defining NDVI computation function...")


def compute_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi.copyProperties(image, ['system:time_start'])


# Load full collection once
collection = (ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
              .filterBounds(region)
              .filterDate("2021-01-01", "2025-12-31")
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
              .map(compute_ndvi))

# Function to compute monthly mean


def monthly_mean(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    monthly = collection.filterDate(start, end).mean()

    stats = monthly.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30000,  # increased scale for faster processing
        maxPixels=1e13
    )

    return ee.Feature(None, {
        'year': year,
        'month': month,
        'ndvi': stats.get('NDVI')
    })


years = ee.List.sequence(2021, 2025)
months = ee.List.sequence(1, 12)

features = years.map(
    lambda y: months.map(
        lambda m: monthly_mean(y, m)
    )
).flatten()

# Convert to FeatureCollection
fc = ee.FeatureCollection(features)

print("Start Earth Engine export task...")

task = ee.batch.Export.table.toDrive(
    collection=fc,
    description='NDVI_Monthly_North_America',
    folder='GEE_Exports',
    fileNamePrefix='ndvi_monthly_2021_2025',
    fileFormat='CSV'
)

task.start()

print("Export task started. Check your Google Drive for the output CSV file.")
print("Task status:", task.status())
print("Task ID:", task.id)
print("Task state:", task.status()['state'])
print("Task error message:", task.status().get(
    'error_message', 'No error message'))
print("Go to https://code.earthengine.google.com/tasks to monitor the task progress.")
