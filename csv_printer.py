import pandas as pd
from csv_reader import read_csv

def print_first_five_columns():
    df = read_csv()
    if df is not None:
        print()
        print(df.iloc[:5, :])
        print()

if __name__ == "__main__":
    print_first_five_columns()
