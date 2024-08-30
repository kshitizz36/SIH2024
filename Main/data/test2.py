import networkx as nx
import folium
import pickle
import numpy as np
from heapq import heappop, heappush
import math

# Load the graph from the pickle file
with open('indian_ocean_graph_with_wind.pickle', 'rb') as f:
    G = pickle.load(f)

# Haversine function remains the same
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

def wind_influence(current_node, next_node, hour, ship_speed):
    """Calculate the wind influence on the travel time between two nodes."""
    u_wind = G.nodes[next_node]['wind_data'][hour]['u-component of wind']
    v_wind = G.nodes[next_node]['wind_data'][hour]['v-component of wind']
    wind_speed = np.sqrt(u_wind**2 + v_wind**2)

    # Calculate the wind direction relative to the ship's course
    ship_heading = np.arctan2(G.nodes[next_node]['pos'][1] - G.nodes[current_node]['pos'][1],
                              G.nodes[next_node]['pos'][0] - G.nodes[current_node]['pos'][0])
    wind_heading = np.arctan2(v_wind, u_wind)

    angle_diff = np.abs(wind_heading - ship_heading)
    if angle_diff > np.pi:
        angle_diff = 2 * np.pi - angle_diff

    # Adjust cost based on wind direction and speed
    if angle_diff < np.pi / 4:
        # Favorable wind
        influence_factor = 1 - (wind_speed / ship_speed)
    elif angle_diff < 3 * np.pi / 4:
        # Crosswind
        influence_factor = 1 + (wind_speed / (2 * ship_speed))
    else:
        # Opposing wind
        influence_factor = 1 + (wind_speed / ship_speed)
    
    return max(0.5, influence_factor)  # Ensure cost doesn't go below 0.5

def clean_graph(G):
    """Reset graph node attributes."""
    for node in G.nodes:
        G.nodes[node]['g'] = float('inf')
        G.nodes[node]['h'] = 0
        G.nodes[node]['f'] = float('inf')
        G.nodes[node]['parent'] = None

def astar_path(G, source, target, ship_speed=20, heuristic=haversine):
    """Find the shortest path between source and target nodes using A* with wind influence."""
    clean_graph(G)

    open_set = []
    heappush(open_set, (0, source))

    G.nodes[source]['g'] = 0
    G.nodes[source]['h'] = heuristic(G.nodes[source]['pos'], G.nodes[target]['pos'])
    G.nodes[source]['f'] = G.nodes[source]['h']

    while open_set:
        _, current = heappop(open_set)

        if current == target:
            path = []
            while current:
                path.append(current)
                current = G.nodes[current]['parent']
            return path[::-1]  # Return reversed path

        current_hour = 0  # Assume we start at hour 0, can be adjusted

        for neighbor in G.neighbors(current):
            distance = haversine(G.nodes[current]['pos'], G.nodes[neighbor]['pos'])
            wind_factor = wind_influence(current, neighbor, current_hour, ship_speed)
            tentative_g = G.nodes[current]['g'] + distance * wind_factor

            if tentative_g < G.nodes[neighbor]['g']:
                G.nodes[neighbor]['parent'] = current
                G.nodes[neighbor]['g'] = tentative_g
                G.nodes[neighbor]['h'] = heuristic(G.nodes[neighbor]['pos'], G.nodes[target]['pos'])
                G.nodes[neighbor]['f'] = G.nodes[neighbor]['g'] + G.nodes[neighbor]['h']

                heappush(open_set, (G.nodes[neighbor]['f'], neighbor))

    return []

# Coordinates for Mumbai (approx) and Kolkata (approx)
source_port = (25.347291, 63.073757)[::-1]  # Mumbai
destination_port = (22.5726, 88.3639)[::-1] # Kolkata

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

# Get the shortest path using the enhanced A* algorithm
shortest_path = astar_path(G, source_node, destination_node, heuristic=haversine)

# Plot the route on Folium map
map_center = [(source_port[1] + destination_port[1]) / 2, (source_port[0] + destination_port[0]) / 2]
m = folium.Map(location=map_center, zoom_start=5)

# Add the shortest path to the map
path_coords = [G.nodes[node]['pos'] for node in shortest_path]
folium.PolyLine(locations=[(y, x) for x, y in path_coords], color='blue', weight=5).add_to(m)

# Add the source and destination markers
folium.Marker(location=(source_port[1], source_port[0]), popup="Mumbai", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=(destination_port[1], destination_port[0]), popup="Kolkata", icon=folium.Icon(color='red')).add_to(m)

# Save the map as an HTML file
m.save("mumbai_to_kolkata_route_map_with_wind.html")
print("Route map saved as 'mumbai_to_kolkata_route_map_with_wind.html'.")

m
