import networkx as nx
import folium
import pickle
import numpy as np

# Load the graph from the pickle file
with open('MainGraph.pickle', 'rb') as f:
    G = pickle.load(f)

# A* Algorithm Implementation
def haversine(coord1, coord2):
    """Calculate the great-circle distance between two points on the Earth."""
    lon1, lat1 = np.radians(coord1)
    lon2, lat2 = np.radians(coord2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

def astar_path(G, source, target):
    """Find the shortest path between source and target nodes using A*."""
    return nx.astar_path(G, source, target, heuristic=lambda n1, n2: haversine(G.nodes[n1]['pos'], G.nodes[n2]['pos']))

# Define source and destination ports (as latitude, longitude tuples)
source_port = (22.854222, 69.089267)[::-1]  # Example coordinates, adjust accordingly
destination_port = (21.614470, 88.574890)[::-1]  # Example coordinates, adjust accordingly

# Find the nearest nodes in the graph to the source and destination coordinates
def find_nearest_node(G, coord):
    closest_node = None
    min_dist = float("inf")
    for node, data in G.nodes(data=True):
        dist = haversine(coord, data['pos'])
        if dist < min_dist:
            closest_node = node
            min_dist = dist
    return closest_node

source_node = find_nearest_node(G, source_port)
destination_node = find_nearest_node(G, destination_port)

# Get the shortest path
shortest_path = astar_path(G, source_node, destination_node)

# Plot the route on Folium map
map_center = [(source_port[1] + destination_port[1]) / 2, (source_port[0] + destination_port[0]) / 2]
m = folium.Map(location=map_center, zoom_start=5)

# Add the shortest path to the map
path_coords = [G.nodes[node]['pos'] for node in shortest_path]
folium.PolyLine(locations=[(y, x) for x, y in path_coords], color='blue', weight=5).add_to(m)

# Add the source and destination markers
folium.Marker(location=(source_port[1], source_port[0]), popup="Source Port", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=(destination_port[1], destination_port[0]), popup="Destination Port", icon=folium.Icon(color='red')).add_to(m)

# Save the map as an HTML file
m.save("route_map.html")
print("Route map saved as 'route_map.html'.")

# Display the map (if running in a Jupyter Notebook or similar environment)
m
