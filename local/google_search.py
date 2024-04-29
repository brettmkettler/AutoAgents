# filename: google_search.py

from googlesearch import search

def google_search(query):
    # the query that you want search for
    search_results = []
    try:
        for url in search(query, num_results=10):
            search_results.append(url)
    except Exception as e:
        print(e)
    return search_results

keywords = input("Enter the keywords you want to search: ")
results = google_search(keywords)
for result in results:
    print(result)