import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_csv():
    project_folder = os.path.dirname(os.path.abspath(__file__))
    csv_filename = "connection_graph.csv"
    csv_path = os.path.join(project_folder, csv_filename)
    
    try:
        logging.info(f"Attempting to load file: {csv_path}")
        df = pd.read_csv(csv_path, low_memory=False, dtype=str)
        df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
        logging.info("The CSV file was loaded successfully.")
        
        def valid_time(time_str):
            try:
                h, m, s = map(int, time_str.split(':'))
                if h > 24 or (h == 24 and m > 59) or (h == 24 and m == 59 and s > 59):
                    return False
                return True
            except ValueError:
                return False

        df = df[df['departure_time'].apply(valid_time)]
        df = df[df['arrival_time'].apply(valid_time)]
        
        logging.info("Rows with invalid time have been removed.")
        
        return df
    except FileNotFoundError:
        logging.error(f"File {csv_filename} not found in project folder.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the CSV file: {e}")
        return None
