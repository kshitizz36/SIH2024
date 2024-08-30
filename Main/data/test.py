import pickle
import networkx as nx

# Load the graph from the pickle file
with open('indian_ocean_graph_with_wind.pickle', 'rb') as f:
    G = pickle.load(f)

def display_all_wind_data(G, x, y):
    """
    Displays all wind data (u and v components) for a given coordinate (x, y)
    from the NetworkX graph.
    """
    node = (x, y)

    if node in G.nodes:
        wind_data = G.nodes[node].get('wind_data', {})
        if wind_data:
            print(f"Wind data for coordinate ({x}, {y}):")
            for forecast_hour, data in wind_data.items():
                u_component = data.get('u-component of wind', 'N/A')
                v_component = data.get('v-component of wind', 'N/A')
                print(f"Hour {forecast_hour}:")
                print(f"  U-component of wind: {u_component} m/s")
                print(f"  V-component of wind: {v_component} m/s")
        else:
            print(f"No wind data available for coordinate ({x}, {y}).")
    else:
        print(f"Coordinate ({x}, {y}) not found in the graph.")

# Example usage:
x, y = 30, -20  # Example coordinates
display_all_wind_data(G, x, y)
