# config.py
# ../config.py
# Configuration file for algorithmic trading project

import os
import datetime

# Database configuration
RAW_DATABASE_PATH = os.path.expanduser("../data/raw_stock_data.db")
CLEANED_DATABASE_PATH = os.path.expanduser("../data/cleaned_stock_data.db")
FORECAST_DATABASE_PATH = os.path.expanduser("../data/forecast_stock_data.db")

# Log directory
LOG_DIRECTORY = os.path.expanduser("../logs")

# Log file paths
DATA_COLLECTION_LOG_FILE = os.path.join(LOG_DIRECTORY, "1_data_collection_last_run_log.txt")
CLEANING_LOG_FILE = os.path.join(LOG_DIRECTORY, "2_clean_and_predict_last_run_log.txt")

# Data directories
COMPLETE_RAW_DATA_DIR = os.path.expanduser("../data/complete_raw_daily_stock_data")

# Tickers CSV files
RUSSELL_3000_CSV = os.path.expanduser("../data/Russell_3000_stock_tickers.csv")
ETFs_CSV = os.path.expanduser("../data/ETFs.csv")

# Boolean flags to determine which tickers to retrieve
RETRIEVE_SP500 = True
RETRIEVE_RUSSELL_3000 = False
RETRIEVE_ETFs = False

# Date range for data retrieval
START_DATE = datetime.date(1999, 1, 1)
END_DATE = datetime.datetime.now().date()
