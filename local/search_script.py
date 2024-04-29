# filename: search_script.py

from googlesearch import search

def google_search(query):
    for url in search(query, num_results=10):
        print(url)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python search_script.py [search query]")
        sys.exit(1)
    query = sys.argv[1]
    google_search(query)