import heapq
from datetime import datetime, timedelta
from csv_reader import read_csv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DAY = 24 * 60 * 60

def time_to_seconds(time_str):
    if time_str.startswith('24'):
        time_str = '00' + time_str[2:]
    
    t = datetime.strptime(time_str, "%H:%M:%S")
    return t.hour * 3600 + t.minute * 60 + t.second


def seconds_to_time(seconds):
    return str(timedelta(seconds=seconds))


def dijkstra(graph, start_stop, end_stop, start_time):
    time = time_to_seconds(start_time)
    travel_times = {vertex: float('inf') for vertex in graph}
    travel_times[start_stop] = 0
    current_times = {vertex: float('inf') for vertex in graph}
    current_times[start_stop] = time
    previous = {vertex: None for vertex in graph}
    travel_details = {vertex: None for vertex in graph}  # Słownik szczegółów podróży
    
    i = 0
    pq = [(travel_times[start_stop], current_times[start_stop], start_stop)] 
    
    while pq:
        if i % 100 == 0:
            logging.info(f"Processed {i} iterations.")
            
        current_travel_time, current_time, current_vertex = heapq.heappop(pq)
        
        if current_vertex == end_stop:
            # Budowanie ścieżki
            path = []
            while current_vertex is not None:
                path.append(current_vertex)
                current_vertex = previous[current_vertex]
            path.reverse()  # Odwróć ścieżkę, bo zaczęliśmy od końca
            # Odtwarzanie szczegółów podróży
            travel_path = []
            for vertex in path:
                travel_path.append(travel_details[vertex])
            return (seconds_to_time(current_travel_time), seconds_to_time(current_time), travel_path)
        
        for neighbor, dep_time, arr_time, company, line in graph.get(current_vertex, []):
            dep_seconds = time_to_seconds(dep_time)
            arr_seconds = time_to_seconds(arr_time)

            if dep_seconds < arr_seconds:
                if current_time < dep_seconds:
                    if current_time < arr_seconds:
                        travel_time = DAY + arr_seconds - current_time  #1
                    else:
                        continue  #4
                else:
                    travel_time = DAY + arr_seconds - current_time  #1
            else:
                if current_time < dep_seconds:
                    if current_time < arr_seconds:
                        travel_time = arr_seconds - current_time  #3
                    else:
                        travel_time = DAY + arr_seconds - current_time  #1
                else:
                    travel_time = 2 * DAY + arr_seconds - current_time  #2
            
            new_travel_time = current_travel_time + travel_time
            if new_travel_time < travel_times[neighbor]:
                travel_times[neighbor] = new_travel_time
                new_time = current_time + travel_time
                if new_time > DAY:
                    new_time -= DAY
                current_times[neighbor] = new_time
                previous[neighbor] = current_vertex  # Ustawiamy poprzednika
                travel_details[neighbor] = (line, dep_time, arr_time, company)  # Przechowujemy szczegóły podróży
                heapq.heappush(pq, (new_travel_time, new_time, neighbor))

        i += 1

    return "No route"


def build_graph(df):
    graph = {}
    
    for _, row in df.iterrows():
        company, line, dep_time, arr_time, start, end = (
            row['company'], row['line'], row['departure_time'], row['arrival_time'], row['start_stop'], row['end_stop']
        )
        
        if start not in graph:
            graph[start] = []
        
        graph[start].append((end, dep_time, arr_time, company, line))
    
    logging.info("Graph created.")
    return graph


if __name__ == "__main__":
    df = read_csv()
    if df is not None:
        start_vertex = 'Rymarska'
        end_vertex = 'Krucza'
        start_time = '12:00:00'
        graph = build_graph(df)
        travel_time, time, travel_path = dijkstra(graph, start_vertex, end_vertex, start_time)
        print(f"Travel time from {start_vertex} to {end_vertex}: {travel_time}. Arrival at {time}.")
        print("Path details:")
        for line, dep_time, arr_time, company in travel_path:
            print(f"Company: {company}, Line: {line}, Departure: {dep_time}, Arrival: {arr_time}")
