import osmnx as ox
import networkx as nx
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
import pickle
import concurrent.futures
import matplotlib.pyplot as plt
import pygrib
import mplcursors
import threading

print("Loading ocean shapefile...")
ocean_shapefile = gpd.read_file('CoastlineData/prototype.shp')

indian_ocean_bounds = Polygon([
    [20, -40], 
    [110, -40],
    [110, 25],  
    [20, 25], 
    [20, -40] 
])


indian_ocean_gdf = gpd.GeoDataFrame(geometry=[indian_ocean_bounds], crs="EPSG:4326")

if ocean_shapefile.crs.to_string() != "EPSG:4326":
    ocean_shapefile = ocean_shapefile.to_crs(epsg=4326)


print("Clipping the ocean shapefile to the Indian Ocean...")
indian_ocean_clip = gpd.clip(ocean_shapefile, indian_ocean_gdf)


print("Saving the clipped Indian Ocean shapefile...")
indian_ocean_clip.to_file('indian_ocean_only.shp')


def generate_grid_points(polygon, spacing):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    x_coords = np.arange(min_x + spacing / 2, max_x, spacing)
    y_coords = np.arange(min_y + spacing / 2, max_y, spacing)
    
    for x in x_coords:
        for y in y_coords:
            point = (x, y)
            if polygon.contains(Point(point)):
                points.append(point)
    
    return points


grid_spacing = 2 


print(f"Generating grid points within each polygon with spacing {grid_spacing}...")
all_points = []
for poly in indian_ocean_clip.geometry:
    if isinstance(poly, Polygon):
        points = generate_grid_points(poly, grid_spacing)
        all_points.extend(points)
    elif isinstance(poly, MultiPolygon):
        for sub_poly in poly.geoms:  
            points = generate_grid_points(sub_poly, grid_spacing)
            all_points.extend(points)


G = nx.Graph()


print("Adding nodes to the graph...")
for point in all_points:
    G.add_node(point, pos=point)


def add_edges_for_point(i, point1):
    edges = []
    for j in range(i + 1, total_points):
        point2 = all_points[j]
        distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        if distance <= radius:
            edges.append((point1, point2, distance))
    return edges


print("Adding edges to the graph based on spatial proximity...")
radius = grid_spacing * 1.5 
total_points = len(all_points)

edges = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(add_edges_for_point, i, all_points[i]) for i in range(total_points)]
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        edges.extend(future.result())
        progress = (i / total_points) * 100
        print(f"\rProgress: {progress:.2f}% completed", end="")


for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

print("\nEdge generation completed.")

grib_file = 'ForecastData/combined_output.grb2'
print(f"Opening GRIB2 file: {grib_file}")
grbs = pygrib.open(grib_file)

total_grbs = len(grbs)
processed_grbs = 0
progress_lock = threading.Lock()

def add_wind_data(grb):
    global processed_grbs

    param_name = grb.parameterName

    if param_name in ['u-component of wind', 'v-component of wind']:
        forecast_hour = grb.forecastTime
        data_values = grb.values
        lats, lons = grb.latlons()

    
        for node in G.nodes():
            lat, lon = node

            lat_idx = (np.abs(lats - lat)).argmin()
            lon_idx = (np.abs(lons - lon)).argmin()


            lat_idx = max(0, min(lat_idx, lats.shape[0] - 1))
            lon_idx = max(0, min(lon_idx, lons.shape[1] - 1))


            if 'wind_data' not in G.nodes[node]:
                G.nodes[node]['wind_data'] = {}
            
            if forecast_hour not in G.nodes[node]['wind_data']:
                G.nodes[node]['wind_data'][forecast_hour] = {}

            G.nodes[node]['wind_data'][forecast_hour][param_name] = data_values[lat_idx, lon_idx]


    with progress_lock:
        processed_grbs += 1
        progress = (processed_grbs / total_grbs) * 100
        print(f"\rAdding GRIB data to graph: {progress:.2f}% completed", end="")

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = list(executor.map(add_wind_data, grbs))

grbs.close()


print("\nSaving the graph with wind data as a pickle file...")
with open('indian_ocean_graph_with_wind.pickle', 'wb') as f:
    pickle.dump(G, f)
print("Graph saved as 'indian_ocean_graph_with_wind.pickle'.")


print("Plotting the graph with tooltips...")

plt.figure(figsize=(12, 8))


pos = nx.get_node_attributes(G, 'pos')


nx.draw(G, pos, node_size=10, node_color='red', edge_color='blue', with_labels=False, font_weight='bold', alpha=0.7)

cursor = mplcursors.cursor(hover=True)

@cursor.connect("add")
def on_add(sel):
    node = sel.index
    node_data = G.nodes[list(G.nodes)[node]]
    lat, lon = node_data['pos']
    tooltip_text = f"Location: ({lat}, {lon})\n"
    
    wind_data = node_data.get('wind_data', {})
    for forecast_hour, data in wind_data.items():
        tooltip_text += f"Hour {forecast_hour}:\n"
        for param, value in data.items():
            tooltip_text += f"{param}: {value:.2f} m/s\n"

    sel.annotation.set_text(tooltip_text)
    sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.8)

plt.title("Graph of Indian Ocean Nodes and Edges with Wind Data")
plt.show()
