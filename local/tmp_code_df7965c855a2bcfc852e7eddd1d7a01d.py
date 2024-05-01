import yfinance as yf

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    return info['currentPrice']


meta_stock_price = get_stock_price("META")
print(f'The stock price of META is: {meta_stock_price}')