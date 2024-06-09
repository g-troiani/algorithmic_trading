# math_formulas.py
# ../math_formulas.py
# Definitions of financial and time formulas

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Function to calculate Mean Absolute Error (MAE)
def calculate_mae(actual, predicted):
    return mean_absolute_error(actual, predicted)

# Function to calculate Mean Squared Error (MSE)
def calculate_mse(actual, predicted):
    return mean_squared_error(actual, predicted)

# Function to calculate Root Mean Squared Error (RMSE)
def calculate_rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

# Function to calculate Sharpe Ratio
def calculate_sharpe_ratio(returns, risk_free_rate_annual, risk_free_rate_daily):
    expected_return = returns.mean() * 252  # Annualize the mean return
    expected_volatility = returns.std() * np.sqrt(252)  # Annualize the volatility
    return (expected_return - risk_free_rate_annual) / expected_volatility  # Calculate Sharpe Ratio
