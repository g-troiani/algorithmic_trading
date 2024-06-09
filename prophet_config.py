# prophet_config.py
# ../prophet_config.py
# Configuration file for Prophet forecasting parameters

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from dateutil.easter import easter

# Paths to databases
CLEANED_DATABASE_PATH = "../data/cleaned_stock_data.db"
FORECAST_DATABASE_PATH = "../data/forecast_stock_data.db"

# Prophet configuration parameters
PROPHET_PARAMS = {
    'growth': 'linear',  # Type of growth ('linear' or 'logistic')
    'seasonality_mode': 'additive',  # 'additive' or 'multiplicative' seasonality
    'n_changepoints': 25,  # Number of potential changepoints in the trend
    'changepoint_range': 0.90,  # Proportion of the history in which changepoints are allowed
    'changepoint_prior_scale': 0.20,  # Flexibility of the trend at changepoints
    'seasonality_prior_scale': 15.0,  # Strength of the seasonality component
    'holidays_prior_scale': 20.0,  # Strength of the holiday effects
    'daily_seasonality': False,  # Whether to include daily seasonality
    'weekly_seasonality': False,  # Whether to include weekly seasonality
    'yearly_seasonality': False,  # Whether to include yearly seasonality
    'interval_width': 0.90,  # Width of the uncertainty intervals
    'uncertainty_samples': 1000,  # Number of simulated draws for uncertainty intervals
    'mcmc_samples': 0  # Number of MCMC samples to draw
}

# Seasonality configuration
SEASONALITY_PARAMS = [
    {"name": "monthly", "period": 30.5, "fourier_order": 12},  # Monthly seasonality
    {"name": "quarterly", "period": 365.25 / 4, "fourier_order": 5, "prior_scale": 15},  # Quarterly seasonality
    {"name": "weekly", "period": 7, "fourier_order": 20},  # Weekly seasonality
    {"name": "yearly", "period": 365.25, "fourier_order": 20}  # Yearly seasonality
]

# Forecast horizon
FORECAST_HORIZON = 60  # days

# Risk-free rate
RISK_FREE_RATE_ANNUAL = 0.0525
RISK_FREE_RATE_DAILY = RISK_FREE_RATE_ANNUAL / 252

# Generate holidays
calendar = USFederalHolidayCalendar()
holidays = calendar.holidays(start='2018-01-01', end='2024-02-28')
good_fridays = pd.to_datetime([easter(y) for y in range(2017, 2024)]) - pd.Timedelta(days=2)
holidays_df = pd.DataFrame({
    'holiday': 'US_public_holiday',
    'ds': pd.to_datetime(holidays),
    'lower_window': 0,
    'upper_window': 1,
})
good_friday_df = pd.DataFrame({
    'holiday': 'Good_Friday',
    'ds': good_fridays,
    'lower_window': 0,
    'upper_window': 1,
})
COVID = pd.DataFrame({
    'holiday': 'COVID',
    'ds': pd.to_datetime(['2020-03-15']),
    'lower_window': -15,
    'upper_window': 15,
})
holidays_df = pd.concat([holidays_df, good_friday_df, COVID], ignore_index=True)
PROPHET_PARAMS['holidays'] = holidays_df
