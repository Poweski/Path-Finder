import pandas as pd
from csv_reader import read_csv

def analyze_csv():
    df = read_csv()
    if df is not None:
        print("Podstawowe informacje o danych:")
        print(df.info())
        
        print("\nSprawdzenie brakujących wartości:")
        print(df.isnull().sum())
        
        print("\nSprawdzenie duplikatów:")
        print(df.duplicated().sum())

if __name__ == "__main__":
    analyze_csv()
