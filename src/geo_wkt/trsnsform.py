from pyproj import Transformer

# input bbox in EPSG:4326 (lon/lat)
bbox= [
-121.8343345,
39.6358715,
-120.5195507,
40.6447996
]

# transformer from EPSG:4326 to EPSG:32610
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)

# transform lower-left corner
x_min, y_min = transformer.transform(bbox[0], bbox[1])
# transform upper-right corner
x_max, y_max = transformer.transform(bbox[2], bbox[3])

bbox_32610 = [x_min, y_min, x_max, y_max]
print(bbox_32610)
