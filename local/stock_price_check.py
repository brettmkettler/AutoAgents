# filename: stock_price_check.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI of Chrome doesn't pop up

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get Yahoo Finance page of Capgemini stock prices
driver.get("https://finance.yahoo.com/quote/CAP.PA")

# Parse the webpage
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Get the current price
price = soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')[0].text

print("The current price of Capgemini stock is: ", price)

# Close the driver
driver.quit()