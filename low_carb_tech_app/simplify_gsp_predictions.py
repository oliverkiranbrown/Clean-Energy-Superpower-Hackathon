import pandas as pd
import json

df = pd.read_csv("data/GSP_predictions_v2.csv")
df = df[["GSPs", "pred_normalized", "pred_sum", "GSPGroup", "area_km2"]]
df.to_csv("./data/gsp_level_predictions.csv", index=False)

geojson_data = json.load(open("./data/gsp_regions_processed.geojson"))

central_location_gsp_group = {}
for gsp_group in df["GSPGroup"].unique():

    selected_geometry = next(
        feature for feature in geojson_data["features"]
        if feature["properties"]["GSPGroup"] == gsp_group
    )

    # Calculate the center of the selected region (example using centroid)
    coordinates = selected_geometry["geometry"]["coordinates"]
    if selected_geometry["geometry"]["type"] == "Polygon":
        # Simplified calculation for a polygon
        longitudes, latitudes = zip(*coordinates[0])  # Unpack first ring of the polygon
    elif selected_geometry["geometry"]["type"] == "MultiPolygon":
        # Use the largest polygon in MultiPolygon
        largest_polygon = max(coordinates, key=lambda p: len(p[0]))
        longitudes, latitudes = zip(*largest_polygon[0])

    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)
    central_location_gsp_group[gsp_group] = {"lat": center_lat, "lon": center_lon}
json.dump(central_location_gsp_group, open("./data/gsp_group_central_location.json", "w"))