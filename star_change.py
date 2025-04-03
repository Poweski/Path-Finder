import heapq
import sys
import math
from utils import *
from csv_reader import read_csv

def haversine(lat1, lon1, lat2, lon2):
    """Calculates the distance in kilometers between two points on Earth."""
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def a_star(graph, start_stop, end_stop, start_time, stop_coords):
    time = time_to_seconds(start_time)
    travel_times = {vertex: float('inf') for vertex in graph}
    travel_times[start_stop] = 0
    previous = {vertex: None for vertex in graph}
    used_connections = {}

    pq = [(0 + haversine(*stop_coords[start_stop], *stop_coords[end_stop]), 0, start_stop, 0, None)]

    while pq:
        _, current_travel_time, current_vertex, current_changes, last_line = heapq.heappop(pq)
        current_time = (current_travel_time + time) % DAY

        if current_vertex == end_stop:
            path = []
            while current_vertex is not None:
                path.append(current_vertex)
                current_vertex = previous[current_vertex]
            path.reverse()

            travel_path = []
            for i in range(len(path) - 1):
                from_stop, to_stop = path[i], path[i + 1]
                if (from_stop, to_stop) in used_connections:
                    travel_path.append(used_connections[(from_stop, to_stop)])
            
            return (seconds_to_time(current_travel_time), seconds_to_time(current_time), travel_path)
        
        for neighbor, dep_time, arr_time, company, line in graph.get(current_vertex, []):
            travel_time = calculate_travel_time(dep_time, arr_time, current_time)
            new_travel_time = current_travel_time + travel_time
            heuristic = haversine(*stop_coords[current_vertex], *stop_coords[end_stop])

            if last_line is None or last_line != line:
                new_changes = current_changes + 1
            else:
                new_changes = current_changes
                
            if new_travel_time < travel_times[neighbor]:
                travel_times[neighbor] = new_travel_time
                previous[neighbor] = current_vertex
                used_connections[(current_vertex, neighbor)] = (current_vertex, neighbor, line, dep_time, arr_time, company)
                heapq.heappush(pq, ((heuristic) + (new_changes*100), new_travel_time, neighbor, new_changes, line))

    return f"No route found from {start_stop} to {end_stop}."

if __name__ == "__main__":
    df = read_csv()
    if df is not None:
        start_vertex = 'Wyszyńskiego'
        end_vertex = 'PL. GRUNWALDZKI'
        start_time = '12:00:00'
        graph, stop_coords = build_graph(df)
        start_time_alg = time.time() 
        result = a_star(graph, start_vertex, end_vertex, start_time, stop_coords)
        end_time_alg = time.time()
        computation_time = end_time_alg - start_time_alg
        
        if isinstance(result, str):
            print(result, file=sys.stderr)
        else:
            travel_time, arrival_time, travel_path = result

            print(f"\nCost function value (travel time in seconds): {time_to_seconds(travel_time)}", file=sys.stderr)
            print(f"Computation time: {computation_time:.6f} seconds", file=sys.stderr)
            print(f"\nTravel time from {start_vertex} to {end_vertex}: {travel_time}. Arrival at {arrival_time}.")

            print_travel_summary(travel_path)
            print_path_details(travel_path)
