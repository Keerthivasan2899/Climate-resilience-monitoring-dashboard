import ee


def get_north():
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0")
    return countries.filter(ee.Filter.inList("ADM0_NAME", [
        "United States of America", "Canada", "Mexico"
    ]))


def get_central():
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0")
    return countries.filter(ee.Filter.inList("ADM0_NAME", [
        "Guatemala", "Belize", "Honduras", "El Salvador",
        "Nicaragua", "Costa Rica", "Panama"
    ]))


def get_south():
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0")
    return countries.filter(ee.Filter.inList("ADM0_NAME", [
        "Brazil", "Argentina", "Chile", "Peru", "Colombia",
        "Venezuela", "Bolivia", "Ecuador", "Paraguay",
        "Uruguay", "Guyana", "Suriname"
    ]))
