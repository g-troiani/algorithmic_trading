##  PROJECT STRUCTURE: ## 


<pre>
algorithmic_trading_project/
├── data_collection/
│   ├── data_collection.py
│   ├── utils.py
├── data_cleaning/
│   ├── data_cleaning.py
├── prediction/
│   ├── prediction.py
├── logs/
│   ├── 1_data_collection_last_run_log.txt
│   ├── 2_clean_and_predict_last_run_log.txt
├── data/
│   ├── ETFs.csv
│   ├── Russell_3000_stock_tickers.csv
│   ├── raw_stock_data.db
│   ├── cleaned_stock_data.db
│   ├── forecast_stock_data.db
│   └── plot_images/
├── config.py
├── prophet_config.py
├── math_formulas.py
├── run_pipeline.py
├── requirements.txt
└── README.md
</pre>




 ## Overview
 
The "algorithmic_trading" repository provides tools and scripts for collecting, cleaning, and predicting stock data using various methods. It includes structured code for data management and forecasting.

## Folder Structure

- ### data_collection/
    - Scripts for data retrieval and utility functions.
- ### data_cleaning/
    - Scripts for data preprocessing and cleaning.
- ### prediction/
    - Scripts for generating stock price predictions.
- ### logs/
    - Log files tracking the execution of data collection and prediction processes.
- ### data/
    - CSV files and databases storing raw, cleaned, and forecasted stock data, including images.
- ### config.py
    - Configuration settings for the project.
- ### prophet_config.py
    - Configuration specific to the Prophet forecasting model.
- ### math_formulas.py
    - Mathematical functions used in various calculations.
- ### run_pipeline.py
    - Script to run the entire data pipeline from collection to prediction.
- ### requirements.txt
    - List of Python dependencies required for the project.
- ### README.md
    - Project description and setup instructions.

## Scripts Description
- ### data_collection/data_collection.py
    - Collects stock data from various sources.
- ### data_collection/utils.py
    - Utility functions for data collection.
- ### data_cleaning/data_cleaning.py
    - Cleans and preprocesses collected stock data.
- ### prediction/prediction.py
    - Generates predictions for stock prices using forecasting models.

## Logs
Logs track the last execution times and statuses of data collection and prediction scripts:

- ### logs/1_data_collection_last_run_log.txt
- ### logs/2_clean_and_predict_last_run_log.txt

## Data
The data/ folder contains:

- ETFs.csv and Russell_3000_stock_tickers.csv: Lists of stock tickers.
- raw_stock_data.db, cleaned_stock_data.db, and forecast_stock_data.db: Databases for different stages of data.
- plot_images/: Images generated during the forecasting process.

## Configuration
- config.py: Main configuration file for setting various parameters.
- prophet_config.py: Configuration for the Prophet forecasting model.


## Running the Project
To run the full pipeline:

1. Ensure all dependencies are installed using requirements.txt.
2. Execute run_pipeline.py to start data collection, cleaning, and prediction.
