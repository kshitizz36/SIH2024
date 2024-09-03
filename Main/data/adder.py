import networkx as nx
import pygrib
import numpy as np
import pickle
import concurrent.futures
import threading
import sys

# Load the graph from the pickle file
with open('indian_ocean_graph_with_wind.pickle', 'rb') as f:
    G = pickle.load(f)

# Load the GRIB2 file
grib_file = 'ForecastData/combined_output.grb2'
print(f"Opening GRIB2 file: {grib_file}")
grbs = pygrib.open(grib_file)

# Initialize progress variables
total_grbs = len(grbs)
processed_grbs = 0
progress_lock = threading.Lock()

# Function to add data from the GRIB file to the graph nodes
def add_grib_data_to_graph(grb):
    global processed_grbs

    param_name = grb.parameterName

    if param_name in ['u-component of wind', 'v-component of wind', 'precipitation rate', 'vertical flux of wind', 'visibility']:
        forecast_hour = grb.forecastTime
        data_values = grb.values
        lats, lons = grb.latlons()

        # Assign the nearest available data to the graph nodes
        for node in G.nodes():
            lat, lon = node
            # Find the closest index in the GRIB data
            lat_idx = np.abs(lats - lat).argmin()
            lon_idx = np.abs(lons - lon).argmin()

            # Ensure indices are within valid range
            lat_idx = max(0, min(lat_idx, lats.shape[0] - 1))
            lon_idx = max(0, min(lon_idx, lons.shape[1] - 1))

            # Store the GRIB data in the node's attribute
            if 'grib_data' not in G.nodes[node]:
                G.nodes[node]['grib_data'] = {}
            
            if forecast_hour not in G.nodes[node]['grib_data']:
                G.nodes[node]['grib_data'][forecast_hour] = {}

            G.nodes[node]['grib_data'][forecast_hour][param_name] = data_values[lat_idx, lon_idx]

    # Update and print progress
    global progress_lock
    with progress_lock:
        processed_grbs += 1
        progress = (processed_grbs / total_grbs) * 100
        print(f"\rAdding GRIB data to graph: {progress:.2f}% completed | Processing {param_name} at forecast hour {forecast_hour}", end="")
        sys.stdout.flush()

# Parallelize the GRIB data addition process using threading to avoid pickling issues
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = list(executor.map(add_grib_data_to_graph, grbs))

grbs.close()

# Save the updated graph as a pickle file
print("\nSaving the updated graph with additional GRIB data as a pickle file...")
with open('indian_ocean_graph_with_additional_grib_data.pickle', 'wb') as f:
    pickle.dump(G, f)
print("Graph saved as 'indian_ocean_graph_with_additional_grib_data.pickle'.")
