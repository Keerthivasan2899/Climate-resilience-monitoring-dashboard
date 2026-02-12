import ee

ee.Initialize(project="gee-climate-dashboard-487203")

# Define North America bounding box (temporary test geometry)
north_america = ee.Geometry.Rectangle([-170, 15, -50, 75])

collection = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
    .filterBounds(north_america) \
    .filterDate("2024-01-01", "2024-03-01") \
    .limit(5)

print("Number of images:", collection.size().getInfo())
