import networkx as nx
import matplotlib.pyplot as plt
import pickle
import mplcursors

# Load the graph from the pickle file
with open('indian_ocean_graph_with_additional_grib_data.pickle', 'rb') as f:
    G = pickle.load(f)

# Print the number of nodes and edges in the graph
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")


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
    d = []
    if wind_data:
        tooltip_text += "Available data:\n"
        for forecast_hour, data in wind_data.items():
            for param, value in data.items():
                print(param)

    sel.annotation.set_text(tooltip_text)
    sel.annotation.get_bbox_patch().set(fc="yellow", alpha=0.8)

plt.title("Graph of Indian Ocean Nodes and Edges with Wind Data")
plt.show()
