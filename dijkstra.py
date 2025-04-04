import heapq
import sys
from utils import *
from csv_reader import read_csv

def dijkstra(graph, start_stop, end_stop, start_time):
    time = time_to_seconds(start_time)
    travel_times = {vertex: float('inf') for vertex in graph}
    travel_times[start_stop] = 0
    previous = {vertex: None for vertex in graph}
    used_connections = {}

    pq = [(0, start_stop)]

    while pq:
        current_travel_time, current_vertex = heapq.heappop(pq)
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

            if new_travel_time < travel_times[neighbor]:
                travel_times[neighbor] = new_travel_time
                previous[neighbor] = current_vertex
                used_connections[(current_vertex, neighbor)] = (current_vertex, neighbor, line, dep_time, arr_time, company)
                heapq.heappush(pq, (new_travel_time, neighbor))

    return f"No route found from {start_stop} to {end_stop}."

if __name__ == "__main__":
    df = read_csv()
    if df is not None:
        start_vertex = 'Wyszyńskiego'
        end_vertex = 'PL. GRUNWALDZKI'
        start_time = '12:00:00'
        graph, _ = build_graph(df)
        start_time_alg = time.time() 
        result = dijkstra(graph, start_vertex, end_vertex, start_time)
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
