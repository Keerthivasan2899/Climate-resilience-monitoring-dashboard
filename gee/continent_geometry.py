def get_americas():
    countries = ee.FeatureCollection("FAO/GAUL/2015/level0")

    americas = countries.filter(
        ee.Filter.inList("ADM0_NAME", [
            "United States of America", "Canada", "Mexico",
            "Guatemala", "Belize", "Honduras", "El Salvador",
            "Nicaragua", "Costa Rica", "Panama",
            "Brazil", "Argentina", "Chile", "Peru", "Colombia",
            "Venezuela", "Bolivia", "Ecuador", "Paraguay",
            "Uruguay", "Guyana", "Suriname"
        ])
    )

    return americas.union().geometry()
