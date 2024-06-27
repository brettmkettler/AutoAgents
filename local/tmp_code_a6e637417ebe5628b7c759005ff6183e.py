import yfinance as yf

# Get the data of the stock
data = yf.Ticker("CAP.PA")

# get the historical prices for this ticker
ticker_df = data.history(period="1d")

# get the last price
last_price = ticker_df['Close'][-1]

print("The last stock price of Capgemini is:", last_price)