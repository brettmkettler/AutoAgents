# filename: get_capgemini_stock_price.py

from alpha_vantage.timeseries import TimeSeries

def get_stock_price():
    ts = TimeSeries(key='YOUR_API_KEY')  # replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    data, _ = ts.get_daily(symbol='CAP.PA')  # Capgemini's stock symbol on Euronext Paris
    print(data)

get_stock_price()