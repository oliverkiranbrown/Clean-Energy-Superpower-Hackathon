import geopandas as gpd 

gdf = gpd.read_file('./data/gsp_regions_20220314.geojson')
#df = df.drop(['geometry'], axis=1)
gdf.to_crs(epsg=4326, inplace=True)
gdf.to_file('./data/gsp_regions_processed.geojson', driver='GeoJSON')