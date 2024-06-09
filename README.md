##  PROJECT STRUCTURE: ## 



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
│   ├── plot_images/
├── config.py
├── prophet_config.py
├── math_formulas.py
├── run_pipeline.py
├── requirements.txt
└── README.md



## 1. Data Collection: ## 

Raw data is stored in raw_stock_data.db.

##  2. Data Cleaning: ## 

Cleaned data is stored in cleaned_stock_data.db.
This database is used as the data source for the prediction step.

## 3. Prediction: ## 

Predictions are stored in forecast_stock_data.db.
Aggregate performance metrics and Sharpe ratios are also stored in this database.# algorithmic_trading
