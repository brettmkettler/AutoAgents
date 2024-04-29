# filename: search_internet.py
from googlesearch import search

# Define the query you want to search for
query = "Python programming"

# Perform the search and print the results
for j in search(query, num=5, stop=5, pause=2):
    print(j)