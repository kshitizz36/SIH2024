import osmnx as ox
import networkx as nx
import folium
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
import pickle
import concurrent.futures
import matplotlib.pyplot as plt

# Load the ocean shapefiless
print("Loading ocean shapefile...")
ocean_shapefile = gpd.read_file('CoastlineData/prototype.shp')

# Define the bounding box for the Indian Ocean (Approximate coordinates)
indian_ocean_bounds = Polygon([
    [20, -40],  # Southwest corner
    [110, -40],  # Southeast corner
    [110, 25],   # Northeast corner
    [20, 25],    # Northwest corner
    [20, -40]    # Close the polygon
])

# Create a GeoDataFrame for the Indian Ocean bounds
indian_ocean_gdf = gpd.GeoDataFrame(geometry=[indian_ocean_bounds], crs="EPSG:4326")

# Ensure the ocean shapefile is in the same CRS as the bounding box
if ocean_shapefile.crs.to_string() != "EPSG:4326":
    ocean_shapefile = ocean_shapefile.to_crs(epsg=4326)

# Clip the ocean shapefile to the Indian Ocean bounds
print("Clipping the ocean shapefile to the Indian Ocean...")
indian_ocean_clip = gpd.clip(ocean_shapefile, indian_ocean_gdf)

# Save the clipped shapefile
print("Saving the clipped Indian Ocean shapefile...")
indian_ocean_clip.to_file('indian_ocean_only.shp')

# Function to generate grid points within a polygon
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

# Grid spacing (distance between points)
grid_spacing = 0.3  # Adjust as needed for denser or sparser grid

# Generate grid points for each polygon in the clipped shapefile
print(f"Generating grid points within each polygon with spacing {grid_spacing}...")
all_points = []
for poly in indian_ocean_clip.geometry:
    if isinstance(poly, Polygon):
        points = generate_grid_points(poly, grid_spacing)
        all_points.extend(points)
    elif isinstance(poly, MultiPolygon):
        for sub_poly in poly.geoms:  # Iterate over each polygon in the MultiPolygon
            points = generate_grid_points(sub_poly, grid_spacing)
            all_points.extend(points)

# Create a graph from the points
G = nx.Graph()

# Add nodes to the graph
print("Adding nodes to the graph...")
for point in all_points:
    G.add_node(point, pos=point)

# Function to add edges in parallel
def add_edges_for_point(i, point1):
    edges = []
    for j in range(i + 1, total_points):
        point2 = all_points[j]
        distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        if distance <= radius:
            edges.append((point1, point2, distance))
    return edges

# Add edges based on spatial proximity using multithreading
print("Adding edges to the graph based on spatial proximity...")
radius = grid_spacing * 1.5  # Define a radius for connecting nearby points
total_points = len(all_points)

edges = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(add_edges_for_point, i, all_points[i]) for i in range(total_points)]
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        edges.extend(future.result())
        # Progress calculation
        progress = (i / total_points) * 100
        print(f"\rProgress: {progress:.2f}% completed", end="")

# Add the edges to the graph
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

print("\nEdge generation completed.")

# Save the graph as a pickle file
print("Saving the graph as a pickle file...")
with open('indian_ocean_graph.pickle', 'wb') as f:
    pickle.dump(G, f)
print("Graph saved as 'indian_ocean_graph.pickle'.")

# Plotting the graph using Matplotlib
print("Plotting the graph...")
plt.figure(figsize=(12, 8))

# Get positions from node attributes
pos = nx.get_node_attributes(G, 'pos')

# Draw the nodes and edges
nx.draw(G, pos, node_size=10, node_color='red', edge_color='blue', with_labels=False, font_weight='bold', alpha=0.7)

# Show the plot
plt.title("Graph of Indian Ocean Nodes and Edges")
plt.show()
