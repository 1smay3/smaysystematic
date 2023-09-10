import pandas as pd
from config.private_config import (
    RAW_STOCK_PRICES_DATABASE_YAHOO_URL,
    STOCK_VOLATILITY_LOOKBACK_BDAYS,
    PROCESSED_STOCK_DATABASE_YAHOO_URL,
)
import os
import time


def _filter_multindex_stock_data_to_one_column(
    dataframe: pd.DataFrame, column: str, level=0
) -> pd.DataFrame:
    all_data = dataframe.iloc[:, dataframe.columns.get_level_values(level) == column]
    all_data.columns = all_data.columns.droplevel(level=level)
    return all_data


def _save_dataframe_to_database_processed_data(
    dataframe: pd.DataFrame, dataframe_name, databse_url: str
):
    file_path = f"{databse_url}\{dataframe_name}"
    dataframe.to_pickle(file_path)

    while not os.path.exists(file_path):
        time.sleep(1)  # Wait for 1 second before checking again

    # If the file exists, print a success message
    if os.path.exists(file_path):
        print(
            f"Dataframe '{dataframe_name}' with shape {dataframe.shape} saving to {databse_url}"
        )
    else:
        print("Error: DataFrame was not saved.")
    return None


# Load Stock Prices
all_stock_data = pd.read_pickle(RAW_STOCK_PRICES_DATABASE_YAHOO_URL)

# Adjusted Prices
stock_close_prices = _filter_multindex_stock_data_to_one_column(all_stock_data, "Close")
_save_dataframe_to_database_processed_data(
    stock_close_prices, "stock_prices", PROCESSED_STOCK_DATABASE_YAHOO_URL
)

# Adjusted Returns
stock_close_returns = stock_close_prices.pct_change(1)
_save_dataframe_to_database_processed_data(
    stock_close_prices, "stock_returns", PROCESSED_STOCK_DATABASE_YAHOO_URL
)

# Stock Volatility
stock_volatility = (
    stock_close_returns.shift(1)
    .rolling(
        STOCK_VOLATILITY_LOOKBACK_BDAYS,
        min_periods=int(STOCK_VOLATILITY_LOOKBACK_BDAYS * 0.8),
    )
    .std()
)
