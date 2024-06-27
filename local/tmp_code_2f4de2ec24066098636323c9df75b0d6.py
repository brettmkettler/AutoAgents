import yfinance as yf

# Define the ticker symbol
tickerSymbol = 'CAP.PA' # CAP.PA is the ticker symbol for Capgemini on Yahoo Finance

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2021-1-1')

# See the last 5 rows of the data
print(tickerDf.tail())