# utils.py
# ../data_collection/utils.py
# Utility functions for data collection

import requests
import pandas as pd
import os
import datetime
import yfinance as yf
from sqlalchemy import Table, Column, Integer, Float, Date, MetaData
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Function to retrieve S&P 500 tickers
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    df = pd.read_html(response.text)[0]
    return df['Symbol'].tolist()

# Function to retrieve Russell 3000 tickers
def get_russell_3000_tickers():
    russell_csv_path = config.RUSSELL_3000_CSV
    if os.path.exists(russell_csv_path):
        df = pd.read_csv(russell_csv_path)
        return df['Company Ticker'].tolist()
    else:
        print("Russell 3000 tickers file not found.")
        return []

# Function to retrieve ETF tickers
def get_ETFs_tickers():
    ETFs_csv_path = config.ETFs_CSV
    if os.path.exists(ETFs_csv_path):
        df = pd.read_csv(ETFs_csv_path)
        return df['Symbol'].tolist()
    else:
        print("ETFs tickers file not found.")
        return []

# Function to retrieve stock data for a given ticker
def get_stock_data(ticker, start_date, end_date):
    if start_date >= end_date:
        raise ValueError(f"Start date {start_date} cannot be after end date {end_date}")
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date, interval="1d", auto_adjust=True)
    return hist[['Open', 'High', 'Low', 'Close', 'Volume']]

# Function to read the last run date from a log file
def read_last_run(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            last_run_str = f.readline().strip().split(": ")[1]
            return datetime.datetime.strptime(last_run_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        return None

# Function to log the last run date to a log file
def log_last_run(log_file):
    with open(log_file, 'w') as f:
        f.write(f"Last run: {datetime.datetime.now()}\n")

# Function to process ticker data in parallel
def process_ticker_data_parallel(ticker, start_date, end_date, engine):
    try:
        print(f"Retrieving data for {ticker}")
        data = get_stock_data(ticker, start_date, end_date)
        if not data.empty:
            save_to_db(data, ticker, engine)
            print(f"Data for {ticker} saved successfully.")
    except Exception as e:
        print(f"Could not retrieve or save data for {ticker}: {e}")
        return ticker
    return None

# Function to save stock data to the database
def save_to_db(data, ticker, engine):
    metadata = MetaData()
    table = Table(
        ticker, metadata,
        Column('Date', Date, primary_key=True),
        Column('Open', Float),
        Column('High', Float),
        Column('Low', Float),
        Column('Close', Float),
        Column('Volume', Integer),
        extend_existing=True
    )
    metadata.create_all(engine)
    
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date
    data.to_sql(ticker, con=engine, if_exists='append', index=False)
