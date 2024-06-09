# prediction.py
# ../prediction/prediction.py
# Script for predicting stock prices using Prophet

import os
import pandas as pd
import time
from datetime import datetime
from prophet import Prophet
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, inspect
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import prophet_config
from math_formulas import calculate_mae, calculate_mse, calculate_rmse, calculate_sharpe_ratio

# Setup and Configuration
data_database_path = prophet_config.CLEANED_DATABASE_PATH
forecast_database_path = prophet_config.FORECAST_DATABASE_PATH
data_engine = create_engine(f'sqlite:///{data_database_path}')
forecast_engine = create_engine(f'sqlite:///{forecast_database_path}')

# Prophet configuration parameters
prophet_params = prophet_config.PROPHET_PARAMS
seasonality_params = prophet_config.SEASONALITY_PARAMS
forecast_horizon = prophet_config.FORECAST_HORIZON
risk_free_rate_annual = prophet_config.RISK_FREE_RATE_ANNUAL
risk_free_rate_daily = prophet_config.RISK_FREE_RATE_DAILY

# Ensure plot_images directory exists
plot_images_dir = os.path.expanduser("../data/plot_images")
if not os.path.exists(plot_images_dir):
    os.makedirs(plot_images_dir)

# Function to process each stock table
def process_stock_table(table_name):
    try:
        stock_data = pd.read_sql_table(table_name, con=data_engine, parse_dates=['Date'])
        stock_data['ds'] = stock_data['Date']
        stock_data['y'] = stock_data['Close']

        # Create and fit the Prophet model
        model = Prophet(**prophet_params)
        for seasonality in seasonality_params:
            model.add_seasonality(**seasonality)
        model.fit(stock_data)

        # Generate future dataframe and make predictions
        future = model.make_future_dataframe(periods=forecast_horizon, freq='D')
        forecast = model.predict(future)

        # Save forecast data to database
        forecast['ticker'] = table_name
        forecast.reset_index(drop=True, inplace=True)
        forecast.to_sql(f"{table_name}_forecast", con=forecast_engine, if_exists='replace', index=False)

        # Save plot of forecast
        fig = model.plot(forecast)
        plot_filepath = os.path.join(plot_images_dir, f"{table_name}_forecast_plot.png")
        fig.savefig(plot_filepath)
        plt.close(fig)

        # Evaluate forecast performance
        forecast_period_data = stock_data[stock_data['ds'] > forecast['ds'].max() - pd.Timedelta(days=forecast_horizon)]
        evaluation_df = forecast.set_index('ds')[['yhat']].join(forecast_period_data.set_index('ds')[['y']], how='inner')
        mae = calculate_mae(evaluation_df['y'], evaluation_df['yhat'])
        mse = calculate_mse(evaluation_df['y'], evaluation_df['yhat'])
        rmse = calculate_rmse(evaluation_df['y'], evaluation_df['yhat'])

        # Calculate Sharpe Ratio
        forecast_returns = forecast['yhat'].pct_change().dropna()
        sharpe_ratio = calculate_sharpe_ratio(forecast_returns, risk_free_rate_annual, risk_free_rate_daily)

        return {
            'ticker': table_name,
            'success': True,
            'metrics': {'MAE': mae, 'MSE': mse, 'RMSE': rmse, 'Sharpe Ratio': sharpe_ratio}
        }
    except Exception as e:
        return {'ticker': table_name, 'success': False, 'error': str(e)}

# Function to process a batch of tables
def process_batch(batch):
    results = []
    with ProcessPoolExecutor() as executor:
        future_to_stock = {executor.submit(process_stock_table, table): table for table in batch}
        for future in as_completed(future_to_stock):
            results.append(future.result())
    return results

# Main function to process tables in batches
def main(start_from_batch=0):
    inspector = inspect(data_engine)
    table_names = inspector.get_table_names()
    
    error_stocks = []
    batch_size = 1
    total_batches = len(table_names) // batch_size + (1 if len(table_names) % batch_size else 0)
    batches = [table_names[i:i + batch_size] for i in range(0, len(table_names), batch_size)]

    for batch_number, batch in enumerate(batches, start=1):
        if batch_number < start_from_batch:
            continue

        print(f"Processing batch {batch_number} of {total_batches}")
        results = process_batch(batch)
        for result in results:
            if result['success']:
                print(f"Processed {result['ticker']} successfully. Metrics: {result['metrics']}")
            else:
                print(f"Error processing {result['ticker']}: {result['error']}")
                error_stocks.append(result['ticker'])

    if error_stocks:
        print("Errors encountered for the following stocks:")
        for stock in error_stocks:
            print(stock)

    # Aggregate performance metrics
    if 'results' in locals():
        performance_metrics = {result['ticker']: result['metrics'] for result in results if result['success']}
        aggregate_performance = pd.DataFrame(performance_metrics).T.mean()

        print("Aggregate Performance Metrics:")
        print(aggregate_performance)

        sns.barplot(x=aggregate_performance.index, y=aggregate_performance.values)
        plt.title("Aggregate Performance Metrics")
        plt.ylabel('Metric Value')
        plt.show()

        # Save aggregate performance metrics to database
        aggregate_performance.reset_index(inplace=True)
        aggregate_performance.rename(columns={'index': 'Metric'}, inplace=True)
        aggregate_performance.to_sql("aggregate_performance_metrics", con=forecast_engine, if_exists='replace', index=False)
        print(f"Aggregate performance metrics saved to database")

        # Plot and save Sharpe Ratios
        sharpe_df = pd.DataFrame({ticker: metrics['Sharpe Ratio'] for ticker, metrics in performance_metrics.items()}, index=['Sharpe Ratio']).T
        sns.barplot(x=sharpe_df.index, y=sharpe_df['Sharpe Ratio'])
        plt.title("Sharpe Ratios of Stocks")
        plt.xticks(rotation=45)
        plt.show()

        sharpe_df.reset_index(inplace=True)
        sharpe_df.rename(columns={'index': 'Ticker'}, inplace=True)
        sharpe_df.to_sql("sharpe_ratios", con=forecast_engine, if_exists='replace', index=False)
        print(f"Sharpe ratios saved to database")

        # Print total processing time
        end_time = time.time()
        total_time_minutes = (end_time - start_time) / 60
        minutes = int(total_time_minutes)
        seconds = int((total_time_minutes - minutes) * 60)
        formatted_time = f"{minutes} minutes and {seconds} seconds"
        print(formatted_time)

if __name__ == "__main__":
    main()
