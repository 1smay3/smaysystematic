# Import packages
import yfinance as yf
import pandas as pd
from config.private_config import RAW_STOCK_PRICES_DATABASE_YAHOO_URL
from config.public_config import YAHOO_STOCK_DOWNLOAD_LIST

# Get the data for this tickers from yahoo finance
data = yf.download(YAHOO_STOCK_DOWNLOAD_LIST, "1900-1-1", "2024-1-1", auto_adjust=True)

data.to_pickle(RAW_STOCK_PRICES_DATABASE_YAHOO_URL)
