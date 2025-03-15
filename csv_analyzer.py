from csv_reader import read_csv
import re

def is_valid_time_format(time_str):
    return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d:00", str(time_str)))
def analyze_csv():
    df = read_csv()
    if df is not None:
        print("\nChecking for missing values:")
        print(df.isnull().sum())
        
        print("\nChecking for duplicates:")
        print(df.duplicated().sum())
        
        if df.shape[1] > 1:
            unique_values = df.iloc[:, 1].dropna().unique()
            print("\nUnique values from the second column:")
            print(unique_values)

        if {'departure_time', 'arrival_time'}.issubset(df.columns):
            invalid_departure = df[~df['departure_time'].apply(is_valid_time_format)]
            invalid_arrival = df[~df['arrival_time'].apply(is_valid_time_format)]
            
            print("\nInvalid values ​​in departure_time:")
            print(invalid_departure)
            
            print("\nInvalid values ​​in arrival_time:")
            print(invalid_arrival)

            starts_with_00_departure = df[df['departure_time'].astype(str).str.startswith('00:')]
            starts_with_00_arrival = df[df['arrival_time'].astype(str).str.startswith('00:')]
            
            print("\nEntries in departure_time starting with 00:")
            print(starts_with_00_departure)
            
            print("\nArrival_time entries starting with 00:")
            print(starts_with_00_arrival)
            

if __name__ == "__main__":
    analyze_csv()
    