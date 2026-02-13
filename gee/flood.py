import ee
from continent_geometry import get_north_america

print("Initializing Earth Engine...")
ee.Initialize(project="gee-climate-dashboard-487203")
print("Earth Engine initialized successfully.")

region = get_north_america()

print("Loading Sentinel-1 SAR dataset...")

# FIXED: Changed 'W' to 'VV'
collection = (ee.ImageCollection("COPERNICUS/S1_GRD")
              .filterBounds(region)
              .filterDate("2021-01-01", "2025-12-31")
              .filter(ee.Filter.eq('instrumentMode', 'IW'))
              .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
              .select('VV'))
print("Sentinel-1 SAR dataset loaded successfully.")


def monthly_flood_area(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    # Filter for the specific month
    month_col = collection.filterDate(start, end)

    # SAFETY CHECK: Only process if images exist for this month
    def compute_area():
        monthly = month_col.median()

        # Identify water (pixels less than -15 dB)
        water = monthly.lt(-15)

        # Calculate area of those pixels
        pixel_area = water.multiply(ee.Image.pixelArea())

        stats = pixel_area.reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=region,
            scale=30000,
            maxPixels=1e13
        )
        # Convert to km2 (divide by 1,000,000)
        return ee.Number(stats.get('VV', 0)).divide(1e6)

    # Use ee.Algorithms.If to return 0 if the month is empty
    area_km2 = ee.Number(ee.Algorithms.If(
        month_col.size().gt(0), compute_area(), 0))

    return ee.Feature(None, {
        'year': year,
        'month': month,
        'flood_area_km2': area_km2
    })


# Generate flood area for each month from 2021 to 2025
years = ee.List.sequence(2021, 2025)
months = ee.List.sequence(1, 12)

features = years.map(
    lambda y: months.map(
        lambda m: monthly_flood_area(y, m)
    )
).flatten()

fc = ee.FeatureCollection(features)

print("Starting flood export task...")

task = ee.batch.Export.table.toDrive(
    collection=fc,
    description='Flood_Monthly_North_America',
    folder='GEE_Exports',
    fileNamePrefix='flood_monthly_2021_2025',
    fileFormat='CSV'
)

task.start()

print("Export task started. Check your Tasks tab: https://code.earthengine.google.com/tasks")
