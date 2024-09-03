import networkx as nx
import pickle
import numpy as np
from heapq import heappop, heappush
from concurrent.futures import ThreadPoolExecutor
from shapely.geometry import LineString, Polygon
import math
from datetime import timedelta, datetime
import folium
from scipy.interpolate import CubicSpline
import json


json_input = '''
{
    "start": [19.0760, 72.8777],
    "end": [13.0827, 80.2707],
    "ship": {
        "shipType": "Cargo",
        "Loa": 2414,
        "Draft": 1241,
        "Displ": 2414,
        "Power": 440,
        "Load": 2200,
        "Speed": 15,
        "Beam": 30
    }
}
'''


input_data = json.loads(json_input)


ship_speed = input_data['ship']['Speed']  
ship_displ = input_data['ship']['Displ']
ship_power = input_data['ship']['Power']
ship_load = input_data['ship']['Load']
ship_beam = input_data['ship']['Beam']


with open('/home/cryptodarth/Cryptd/Smart-India-Hackathon-2024/Main/data/indian_ocean_graph_with_wind.pickle', 'rb') as f:
    G = pickle.load(f)


base_speed = ship_speed  
start_time = datetime(2024, 8, 29, 6, 0)  


def effective_speed(base_speed, u_wind, v_wind, travel_direction, ship_displ, ship_power, ship_load, ship_beam):
    wind_speed = np.sqrt(u_wind**2 + v_wind**2)
    wind_direction = np.degrees(np.arctan2(v_wind, u_wind)) % 360

    angle_diff = abs(wind_direction - travel_direction)
    wind_parallel = wind_speed * np.cos(np.radians(angle_diff))


    wind_resistance = wind_parallel * (ship_beam / 10) / ship_displ  


    power_factor = ship_power / 500.0  
    load_factor = ship_load / 3000.0  
    effective_speed = base_speed + (power_factor - load_factor) * base_speed - wind_resistance

    return max(0, effective_speed)  

def fuel_consumption(speed, power, distance):
    
    if speed <= 0:
        return float('inf')  

    consumption_rate = (power / speed) * 0.1  
    return consumption_rate * distance

def haversine(coord1, coord2):
    lon1, lat1 = np.radians(coord1)
    lon2, lat2 = np.radians(coord2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance_km = 6371 * c  
    distance_nautical_miles = distance_km * 0.53996  
    return distance_nautical_miles, distance_km  

def clean_graph(G):
    for node in G.nodes:
        G.nodes[node]['g'] = float('inf')
        G.nodes[node]['h'] = 0
        G.nodes[node]['f'] = float('inf')
        G.nodes[node]['parent'] = None
        G.nodes[node]['cumulative_time'] = None  
        G.nodes[node]['cumulative_fuel'] = 0  
        G.nodes[node]['cumulative_distance'] = 0  

def wind_aware_heuristic(coord1, coord2, wind_data, travel_direction, ship_displ, ship_power, ship_load, ship_beam, g_cost):
    distance, _ = haversine(coord1, coord2)

    u_wind = wind_data['u-component of wind']
    v_wind = wind_data['v-component of wind']

    wind_speed = np.sqrt(u_wind**2 + v_wind**2)
    wind_direction = np.degrees(np.arctan2(v_wind, u_wind)) % 360

    angle_diff = abs(wind_direction - travel_direction)

    wind_parallel = wind_speed * np.cos(np.radians(angle_diff))
    effective_distance = distance / (1 + wind_parallel / base_speed)


    h_cost = fuel_consumption(effective_distance, ship_power, distance)

    return g_cost + h_cost


def astar_path(G, source, target, base_speed, start_time, ship_displ, ship_power, ship_load, ship_beam):
    clean_graph(G)

    open_set = []
    heappush(open_set, (0, source))

    G.nodes[source]['g'] = 0
    G.nodes[source]['h'] = wind_aware_heuristic(G.nodes[source]['pos'], G.nodes[target]['pos'], G.nodes[source]['wind_data'][0], 0, ship_displ, ship_power, ship_load, ship_beam, G.nodes[source]['g'])
    G.nodes[source]['f'] = G.nodes[source]['h']
    G.nodes[source]['cumulative_time'] = 0

    closed_set = set()

    while open_set:
        _, current = heappop(open_set)

        if current == target:
            path = []
            times = []
            total_distance = G.nodes[current]['cumulative_distance']  
            fuel_consumed = G.nodes[current]['cumulative_fuel']
            while current:
                path.append(current)
                times.append(G.nodes[current]['cumulative_time'])
                current = G.nodes[current]['parent']
            return path[::-1], times[::-1], total_distance, fuel_consumed  

        if current in closed_set:
            continue

        closed_set.add(current)

        neighbors = list(G.neighbors(current))

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(process_neighbor, G, current, neighbor, target, base_speed, ship_displ, ship_power, ship_load, ship_beam): neighbor
                for neighbor in neighbors
            }
            for future in futures:
                tentative_g = future.result()
                neighbor = futures[future]
                if tentative_g is not None:
                    heappush(open_set, (G.nodes[neighbor]['f'], neighbor))

    return [], [], 0, 0

def process_neighbor(G, current, neighbor, target, base_speed, ship_displ, ship_power, ship_load, ship_beam):
    current_pos = G.nodes[current]['pos']
    neighbor_pos = G.nodes[neighbor]['pos']

    travel_direction = np.degrees(np.arctan2(neighbor_pos[1] - current_pos[1], neighbor_pos[0] - current_pos[0]))

    distance, distance_km = haversine(current_pos, neighbor_pos)
    current_cumulative_time = G.nodes[current]['cumulative_time']
    current_cumulative_fuel = G.nodes[current]['cumulative_fuel']
    current_cumulative_distance = G.nodes[current]['cumulative_distance']

    travel_time = distance / base_speed
    cumulative_time_at_neighbor = current_cumulative_time + travel_time
    hours_since_start = int(cumulative_time_at_neighbor)

    wind_data = None
    try:
        wind_data = G.nodes[neighbor]['wind_data'][hours_since_start]
    except KeyError:
        wind_data = {'u-component of wind': 0, 'v-component of wind': 0}
    except IndexError:
        wind_data = G.nodes[neighbor]['wind_data'][max(G.nodes[neighbor]['wind_data'].keys())]

    u_wind = wind_data['u-component of wind']
    v_wind = wind_data['v-component of wind']

    eff_speed = effective_speed(base_speed, u_wind, v_wind, travel_direction, ship_displ, ship_power, ship_load, ship_beam)
    travel_time = distance / eff_speed if eff_speed > 0 else float('inf')

    fuel_used = fuel_consumption(eff_speed, ship_power, distance)
    cumulative_fuel_at_neighbor = current_cumulative_fuel + fuel_used
    cumulative_distance_at_neighbor = current_cumulative_distance + distance_km

    tentative_g = G.nodes[current]['g'] + travel_time
    cumulative_time_at_neighbor = current_cumulative_time + travel_time

    if tentative_g < G.nodes[neighbor]['g']:
        G.nodes[neighbor]['parent'] = current
        G.nodes[neighbor]['g'] = tentative_g
        G.nodes[neighbor]['h'] = wind_aware_heuristic(neighbor_pos, G.nodes[target]['pos'], wind_data, travel_direction, ship_displ, ship_power, ship_load, ship_beam, tentative_g)
        G.nodes[neighbor]['f'] = G.nodes[neighbor]['g'] + G.nodes[neighbor]['h']
        G.nodes[neighbor]['cumulative_time'] = cumulative_time_at_neighbor
        G.nodes[neighbor]['cumulative_fuel'] = cumulative_fuel_at_neighbor  
        G.nodes[neighbor]['cumulative_distance'] = cumulative_distance_at_neighbor  
        return tentative_g
    return None

def find_nearest_node(G, coord):
    closest_node = None
    min_dist = float("inf")
    for node, data in G.nodes(data=True):
        dist = haversine(coord, data['pos'])[0]  
        if dist < min_dist:
            closest_node = node
            min_dist = dist
    return closest_node


def main(start,end):

    start_port = tuple(start[::-1])  
    end_port = tuple(end[::-1])
    source_node = find_nearest_node(G, start_port)
    destination_node = find_nearest_node(G, end_port)

    shortest_path, cumulative_times, total_distance, fuel_consumed = astar_path(G, source_node, destination_node, base_speed, start_time, ship_displ, ship_power, ship_load, ship_beam)

    final_time = cumulative_times[-1] if cumulative_times else 0  # time in hrs


    total_hours = int(final_time)
    total_minutes = int((final_time - total_hours) * 60)

    eta = start_time + timedelta(hours=total_hours, minutes=total_minutes)


    print(f"Total travel time according to the algorithm: {total_hours} hours and {total_minutes} minutes")
    print(f"Estimated Time of Arrival (ETA): {eta.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Estimated Fuel Consumption: {fuel_consumed:.2f} units")
    print(f"Total Distance to be covered: {total_distance:.2f} kilometers")

    path_coords = [G.nodes[node]['pos'] for node in shortest_path]



    if len(path_coords) > 2:
        x, y = zip(*path_coords)
        cs = CubicSpline(range(len(x)), np.array([x, y]), axis=1)
        fine_t = np.linspace(0, len(x)-1, num=len(x)*10)
        refined_coords = list(zip(cs(fine_t)[0], cs(fine_t)[1]))
    else:
        refined_coords = path_coords  


    map_center = [(start_port[1] + end_port[1]) / 2, (start_port[0] + end_port[0]) / 2]
    m = folium.Map(location=map_center, zoom_start=5)
    x = str(eta.strftime('%Y-%m-%d %H:%M:%S'))

    d = [(y, x) for x, y in refined_coords]
    fc = [start]
    fc.extend(d)
    fc.append(end)
    return [fc,final_time,total_distance,fuel_consumed,map_center]