import ee


def get_north_america():
    # Simplified bounding box for NA(smaller extent for testing)
    return ee.Geometry.Rectangle([-140, 20, -60, 60])
