import ee
from continent_geometry import get_north_america

print("Initializing Earth Engine...")
ee.Initialize(project="gee-climate-dashboard-487203")
print("Earth Engine initialized successfully.")

print("Getting North America geometry...")
region = get_north_america()

# Cloud mask function

print("Defining cloud masking function...")


def mask_s2_clouds(image):
    qa = image.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
        qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    return image.updateMask(mask)

# NDVI function


print("Defining NDVI computation function...")


def compute_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi.copyProperties(image, ['system:time_start'])


# Load Sentinel-2

start_date = ee.Date("2024-07-01")
end_date = ee.Date("2024-08-01")

print("Loading Sentinel-2 collection...")
collection = (ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
              .filterBounds(region)
              .filterDate(start_date, end_date)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
              .map(compute_ndvi))


# Check collection size first

print("Checking image count...")
count = collection.size().getInfo()
print("Image count:", count)

if count == 0:
    print("No images found for this period.")
else:
    print("Computing monthly mean NDVI...")
    monthly_ndvi = collection.mean()

    print("Reducing region (this may take a while)...")
    stats = monthly_ndvi.reduceRegion(reducer=ee.Reducer.mean(),
                                      geometry=region,
                                      scale=20000,
                                      maxPixels=1e13
                                      )

    print("Fetching results from Earth Engine...")
    result = stats.getInfo()

    print("Mean NDVI result:", result)

print("Process completed.")
