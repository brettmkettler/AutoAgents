# filename: stock_price.py

import requests
from bs4 import BeautifulSoup

def get_stock_price(company_name):
    url = f"https://www.google.com/search?q={company_name}+stock+price"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    price = soup.find('div', attrs={'class':'BNeawe iBp4i AP7Wnd'}).get_text()
    
    print(f"The current stock price of {company_name} is: {price}")

get_stock_price("Capgemini")