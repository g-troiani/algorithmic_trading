# data_cleaning.py
# ../data_cleaning/data_cleaning.py
# Script for cleaning stock data

import os
import pandas as pd
import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, Date, inspect
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Setup and Configuration
source_database_path = config.RAW_DATABASE_PATH
cleaned_database_path = config.CLEANED_DATABASE_PATH
log_directory = config.LOG_DIRECTORY
log_file = config.CLEANING_LOG_FILE

# Ensure log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Initialize SQLite engines
source_engine = create_engine(f'sqlite:///{source_database_path}')
cleaned_engine = create_engine(f'sqlite:///{cleaned_database_path}')
metadata = MetaData()

start_date = pd.to_datetime('2018-01-01').tz_localize('US/Eastern')
end_date = pd.to_datetime(datetime.datetime.now(), utc=True).tz_convert('US/Eastern')

# Global counter and its lock
global_counter = 0
counter_lock = Lock()

# Function to read the last run date from a log file
def read_last_run(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            last_run_str = f.readline().strip().split(": ")[1]
            return datetime.datetime.strptime(last_run_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        return None

# Function to process a single table (stock data)
def process_table(table_name):
    global global_counter
    df = pd.read_sql_table(table_name, con=source_engine, parse_dates=['Date'], index_col='Date')
    df.index = df.index.tz_localize('US/Eastern', ambiguous='infer')
    df = df[['Open', 'Close']]

    # Handle duplicate dates by averaging
    if df.index.duplicated().any():
        df = df.groupby(df.index).mean()

    # Filter for dates within the specified range
    df = df[(df.index >= start_date) & (df.index <= end_date)]

    # Resample to daily frequency, filling missing dates
    df_daily = df.resample('D').asfreq()

    # Interpolate weekend values
    for date, row in df_daily.iterrows():
        if date.weekday() in [5, 6]:  # Saturday or Sunday
            if pd.isna(row['Close']):
                df_daily.at[date, 'Close'] = df_daily.at[date - pd.DateOffset(days=date.weekday() - 4), 'Close']
            if pd.isna(row['Open']):
                next_monday = date + pd.DateOffset(days=7 - date.weekday())
                if next_monday in df_daily.index:
                    df_daily.at[date, 'Open'] = df_daily.at[next_monday, 'Open']

    # Interpolate other missing values linearly for 'Close' prices
    df_daily['Close'] = df_daily['Close'].interpolate(method='linear')

    # Drop the 'Open' column
    df_daily = df_daily.drop(columns=['Open'])

    # Update the global counter within a thread-safe block
    with counter_lock:
        global_counter += 1
        local_counter = global_counter

    # Save the cleaned data to the new database
    df_daily.reset_index(inplace=True)
    df_daily['Date'] = df_daily['Date'].dt.date
    df_daily.to_sql(table_name, con=cleaned_engine, if_exists='replace', index=False)
    print(f"{local_counter}) Processed data saved to table {table_name}")

# Main function to process tables in parallel
def main():
    start_time = time.time()
    last_run = read_last_run(log_file)

    inspector = inspect(source_engine)
    table_names = inspector.get_table_names()
    
    # Using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_table, table_name): table_name for table_name in table_names}
        error_tables = [futures[future] for future in as_completed(futures) if future.result() is not None]

    print("Processing complete.")
    if error_tables:
        print(f"Total number of errors: {len(error_tables)}")
        print("Tables with errors:")
        print('\n'.join(error_tables))
    else:
        print("No errors encountered.")

    # Log the completion of data cleaning
    with open(log_file, 'w') as f:
        f.write(f"Last run: {datetime.datetime.now()}")

    end_time = time.time()
    total_time = (end_time - start_time) / 60
    print(f"Total processing time: {int(total_time)} minutes and {int((total_time - int(total_time)) * 60)} seconds")

if __name__ == "__main__":
    main()
