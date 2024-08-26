import geopandas as gpd
from shapely.geometry import box

# Define the bounding box for the Indian Ocean based on the provided coordinates
minx, miny = 20.0026, -60.0     # Minimum longitude and latitude
maxx, maxy = 146.8982, 31.1859  # Maximum longitude and latitude

# Create a bounding box polygon
bounding_box = box(minx, miny, maxx, maxy)

# Load the input shapefile
input_shapefile = "coastline/lines.shp"  # Replace with your actual shapefile path
gdf = gpd.read_file(input_shapefile)

# Clip the shapefile to the bounding box of the Indian Ocean
clipped_gdf = gpd.clip(gdf, bounding_box)

# Save the clipped shapefile
output_shapefile = "clipped_indian_ocean_shapefile2.shp"
clipped_gdf.to_file(output_shapefile)

print(f"Clipped shapefile saved as {output_shapefile}")
