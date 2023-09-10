import alpaca_trade_api as tradeapi
from config.alpaca.api_keys import ALPACA_PUBLIC_KEY, ALPACA_SECRET_KEY

# authentication and connection details
base_url = "https://paper-api.alpaca.markets"

# instantiate REST API
api = tradeapi.REST(ALPACA_PUBLIC_KEY, ALPACA_SECRET_KEY, base_url, api_version="v2")

# obtain account information
account = api.get_account()
print(account)
