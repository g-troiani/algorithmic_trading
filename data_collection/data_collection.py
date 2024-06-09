# data_collection.py
# ../data_collection/data_collection.py
# Script for collecting stock data

import yfinance as yf
import pandas as pd
import requests
import os
import datetime
import time
import concurrent.futures
from sqlalchemy import create_engine, MetaData
from utils import get_sp500_tickers, get_russell_3000_tickers, get_ETFs_tickers, get_stock_data, read_last_run, log_last_run, process_ticker_data_parallel
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Setup and Configuration
database_path = config.RAW_DATABASE_PATH
log_directory = config.LOG_DIRECTORY
log_file = config.DATA_COLLECTION_LOG_FILE

# Ensure log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Initialize SQLite engine
engine = create_engine(f'sqlite:///{database_path}')
metadata = MetaData()

# Determine the start date for data collection
last_run_date = read_last_run(log_file)
start_date = (last_run_date + datetime.timedelta(days=1)).date() if last_run_date else config.START_DATE
current_date = datetime.datetime.now().date()

# Ensure start_date is before current_date
if start_date >= current_date:
    start_date = current_date - datetime.timedelta(days=1)

# Fetch Tickers based on configuration
combined_tickers = []

if config.RETRIEVE_SP500:
    sp500_tickers = [ticker.replace('.', '-') for ticker in get_sp500_tickers()]
    combined_tickers.extend(sp500_tickers)

if config.RETRIEVE_RUSSELL_3000:
    russell_3000_tickers = [ticker.replace('.', '-') for ticker in get_russell_3000_tickers()]
    combined_tickers.extend(russell_3000_tickers)

if config.RETRIEVE_ETFs:
    ETFs_tickers = [ticker.replace('.', '-') for ticker in get_ETFs_tickers()]
    combined_tickers.extend(ETFs_tickers)

combined_tickers = list(set(combined_tickers))  # Remove duplicates

# Parallel Processing of Tickers
start_time = time.time()
tickers_without_data = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_ticker_data_parallel, ticker, start_date, current_date, engine): ticker for ticker in combined_tickers}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            tickers_without_data.append(result)

print('Tickers without data:', len(tickers_without_data))
print(tickers_without_data)

# Log the completion of data collection
log_last_run(log_file)
print("Data collection complete.")
