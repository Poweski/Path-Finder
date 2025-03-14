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
        return df
    except FileNotFoundError:
        logging.error(f"File {csv_filename} not found in project folder.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the CSV file: {e}")
        return None
