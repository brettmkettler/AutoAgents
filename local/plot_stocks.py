# filename: plot_stocks.py

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Download history data for TSLA and FB
tsla = yf.Ticker("TSLA")
fb = yf.Ticker("META")

# Get historical market data starting from 2024-01-01
hist_tsla = tsla.history(start="2024-01-01", end="2024-04-11")
hist_fb = fb.history(start="2024-01-01", end="2024-04-11")

# Calculate daily returns
hist_tsla['daily_return'] = hist_tsla['Close'].pct_change()
hist_fb['daily_return'] = hist_fb['Close'].pct_change()

# Calculate cumulative returns
hist_tsla['cumulative_return'] = (1 + hist_tsla['daily_return']).cumprod()
hist_fb['cumulative_return'] = (1 + hist_fb['daily_return']).cumprod()

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot data
hist_tsla['cumulative_return'].plot(ax=ax, label='TSLA')
hist_fb['cumulative_return'].plot(ax=ax, label='META')

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Return')
plt.title('TSLA vs META YTD Returns')

# Place a legend on the axes
plt.legend()

# Save the figure
plt.savefig('stock_gains.png')

print("Plot saved as 'stock_gains.png'")