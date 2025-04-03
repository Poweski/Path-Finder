from datetime import datetime, timedelta
import logging
import time

DAY = 24 * 60 * 60

start_time_program = time.time() 

def time_to_seconds(time_str):
    if time_str.startswith('24'):
        time_str = '00' + time_str[2:]
    
    t = datetime.strptime(time_str, "%H:%M:%S")
    return t.hour * 3600 + t.minute * 60 + t.second

def seconds_to_time(seconds):
    return str(timedelta(seconds=seconds))

def build_graph(df):
    graph = {}
    stop_coords = {}

    REQUIRED_COLUMNS = { 'company', 'line', 'departure_time', 'arrival_time', 'start_stop', 'end_stop', 
                        'start_stop_lat', 'start_stop_lon', 'end_stop_lat', 'end_stop_lon'}
    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("DataFrame is missing required columns")

    logging.info("Creating graph")
    for _, row in df.iterrows():
        company, line, dep_time, arr_time, start, end, start_lat, start_lon, end_lat, end_lon = (
            row['company'], row['line'], row['departure_time'], row['arrival_time'], row['start_stop'], 
            row['end_stop'], row['start_stop_lat'], row['start_stop_lon'], row['end_stop_lat'], row['end_stop_lon']
        )

        if start not in graph:
            graph[start] = []
        if end not in stop_coords:
            stop_coords[end] = (end_lat, end_lon)
        if start not in stop_coords:
            stop_coords[start] = (start_lat, start_lon)

        graph[start].append((end, dep_time, arr_time, company, line))
        logging.debug(f"Added edge: {start} -> {end} ({company}, {line}, {dep_time}-{arr_time})")

    logging.info("Graph created successfully")
    return graph, stop_coords

def calculate_travel_time(dep_time, arr_time, current_time):
    dep_seconds = time_to_seconds(dep_time)
    arr_seconds = time_to_seconds(arr_time)

    if dep_seconds < arr_seconds:
        if current_time < dep_seconds:
            return arr_seconds - current_time
        else:
            return DAY + arr_seconds - current_time
    else:
        if current_time < dep_seconds:
            return DAY + arr_seconds - current_time
        else:
            return 2 * DAY + arr_seconds - current_time

def print_travel_summary(travel_path):
    """Lists the places where lines change on the travel route."""
    prev_line = None
    start_stop = None
    start_time = None
    end_time = None

    for i in range(len(travel_path)):
        current_start_stop, current_end_stop, current_line, current_dep_time, current_arr_time, company = travel_path[i]

        if prev_line is None:
            prev_line = current_line
            start_stop = current_start_stop
            start_time = current_dep_time
            end_time = current_arr_time
        elif prev_line != current_line:
            print(f"({prev_line}, {start_time} {start_stop} -> {end_time} {travel_path[i-1][1]})")
            prev_line = current_line
            start_stop = current_start_stop
            start_time = current_dep_time
            end_time = current_arr_time
        else:
            end_time = current_arr_time

    if prev_line:
        print(f"({prev_line}, {start_time} {start_stop} -> {end_time} {current_end_stop})")

def print_path_details(travel_path):
    print("\nPath details:")
    for start, end, line, dep_time, arr_time, company in travel_path:
        print(f"From: {start} To: {end} | Company: {company}, Line: {line}, Departure: {dep_time}, Arrival: {arr_time}")
