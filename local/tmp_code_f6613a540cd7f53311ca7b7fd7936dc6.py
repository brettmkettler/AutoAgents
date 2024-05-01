import requests
import json

def get_stock_price(symbol):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    base_url = "https://www.alphavantage.co/query?"
    function = "GLOBAL_QUOTE"
    final_url = base_url + "function=" + function + "&symbol=" + symbol + "&apikey=" + api_key
    response = requests.get(final_url)
    data = response.json()
    return data["Global Quote"]["05. price"]

print("The stock price of META is: ", get_stock_price("META"))