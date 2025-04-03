import pandas as pd # type: ignore
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def valid_time(time_str):
    """Function validating time in HH:MM:SS format."""
    try:
        h, m, s = map(int, time_str.split(':'))
        if h > 24 or (h == 24 and m > 59) or (h == 24 and m == 59 and s > 59):
            return False
        return True
    except ValueError:
        return False

def read_csv():
    """A function that reads a CSV file and filters invalid times."""
    project_folder = os.path.dirname(os.path.abspath(__file__))
    csv_filename = "connection_graph.csv"
    csv_path = os.path.join(project_folder, csv_filename)

    try:
        logging.info(f"Attempting to load file: {csv_path}")
        df = pd.read_csv(csv_path, low_memory=False, dtype=str)
        
        # Checking if required columns exist in CSV
        required_columns = ['company', 'line', 'departure_time', 'arrival_time', 'start_stop', 'end_stop', 
                            'start_stop_lat', 'start_stop_lon', 'end_stop_lat', 'end_stop_lon']
        if not all(col in df.columns for col in required_columns):
            logging.error(f"CSV file is missing required columns: {', '.join(required_columns)}")
            return None
        
        #   
        df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
        logging.info("The CSV file was loaded successfully")
        
        # Filtering out invalid times
        df = df[df['departure_time'].apply(valid_time)]
        df = df[df['arrival_time'].apply(valid_time)]
        
        logging.info("Rows with invalid time have been removed")
        
        return df
    except FileNotFoundError:
        logging.error(f"File {csv_filename} not found in project folder")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the CSV file: {e}")
        return None

if __name__ == "__main__":
    df = read_csv()
    if df is not None:
        print(df.head())
    else:
        print("Error")
