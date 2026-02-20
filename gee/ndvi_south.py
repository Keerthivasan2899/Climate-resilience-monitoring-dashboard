import ee
from continent_geometry import get_south

ee.Initialize(project="gee-climate-dashboard-487203")

region = get_south()

collection = (
    ee.ImageCollection("MODIS/061/MOD13Q1")
    .select("NDVI")
    .filterDate("2021-01-01", "2025-12-31")
    .filterBounds(region)
)


def monthly_ndvi(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, "month")

    img = collection.filterDate(start, end).mean()

    stats = img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region.geometry(),
        scale=5000,
        maxPixels=1e13
    )

    return ee.Feature(None, {
        "year": year,
        "month": month,
        "ndvi": stats.get("NDVI")
    })


years = ee.List.sequence(2021, 2025)
months = ee.List.sequence(1, 12)

features = years.map(lambda y: months.map(
    lambda m: monthly_ndvi(y, m))).flatten()
fc = ee.FeatureCollection(features)

task = ee.batch.Export.table.toDrive(
    collection=fc,
    description="NDVI_North_America",
    folder="GEE_Exports",
    fileNamePrefix="ndvi_north_2021_2025",
    fileFormat="CSV"
)

task.start()
print("South America NDVI export started")
