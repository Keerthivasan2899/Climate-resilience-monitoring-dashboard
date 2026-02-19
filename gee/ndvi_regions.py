import ee
from continent_geometry import get_americas

print("Initializing Earth Engine...")
ee.Initialize(project="gee-climate-dashboard-487203")
print("Earth Engine Initialized successfully")

region = get_americas

# ------------------------
# Load Sentinel-2 NDVI
# ------------------------


def compute_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return ndvi.copyProperties(image, ['system:time_start'])


collection = (ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
              .filterDate("2021-01-01", "2025-12-31")
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
              .map(compute_ndvi))

# -------------------------
# Country boundaries
# -------------------------
countries = ee.FeatureCollection("FAO/GAUL/2015/level0")

north = countries.filter(ee.Filter.inList("ADM0_NAME", [
    "United States of America", "Canada"
]))

central = countries.filter(ee.Filter.inList("ADM0_NAME", [
    "Mexico", "Guatemal", "Belize", "Hounduras", "El Salvador",
    "Nicaragua", "Costa Rica", "Panama"
]))

south = countries.filter(ee.Filter.inList("ADM0_NAME", [
    "Brazil", "Argentina", "Chile", "Peru", "Colombia", "Venezuela",
    "Bolivia", "Ecuador", "Paraguay", "Uruguay", "Guyana", "Suriname"
]))

regions = [
    ("North America", north),
    ("Central America", central),
    ("South America", south)
]

# --------------------------
# Monthly stats per region
# --------------------------


def monthly_stats(year, month):

    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    monthly = collection.filterDate(start, end).mean()

    feats = []

    for name, geom in regions:
        stats = monthly.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geom.geometry(),
            scale=5000,
            maxPixels=1e13
        )

        feats.append(
            ee.Feature(None, {
                "year": year,
                "month": month,
                "region": name,
                "ndvi": stats.get("NDVI")
            })
        )
    return ee.FeatureCollection(feats)


# -------------------------
# Build full dataset
# -------------------------
years = ee.List.sequence(2021, 2025)
months = ee.List.sequence(1, 12)

features = years.map(
    lambda y: months.map(
        lambda m: monthly_stats(y, m)
    )
).flatten()

fc = ee.FeatureCollection(features).flatten()

# -------------------------
# Export
# -------------------------
regions = [
    ("North_America", north),
    ("Central_America", central),
    ("South_America", south)
]

for name, geom in regions:

    def monthly_mean(year, month):
        start = ee.Date.fromYMD(year, month, 1)
        end = start.advance(1, 'month')

        monthly = collection.filterDate(start, end).mean()

        stats = monthly.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=geom,
            scale=30000,
            maxPixels=1e13
        )

        return ee.Feature(None, {
            'region': name,
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

    fc = ee.FeatureCollection(features)

    task = ee.batch.Export.table.toDrive(
        collection=fc,
        description=f"NDVI_{name}",
        folder="GEE_Exports",
        fileNamePrefix=f'ndvi_{name.lower()}_2021_2025',
        fileFormat='CSV'
    )

    task.start()
    print(f"Exporting NDVI data for {name} to Google Drive...")
