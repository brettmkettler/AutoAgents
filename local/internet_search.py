# filename: internet_search.py
from googlesearch import search

def search_internet(query):
    for url in search(query, num_results=10):
        print(url)

search_internet("Python scripting")