   # filename: internet_search.py
   
   from googlesearch import search

   def google_search(query):
       for url in search(query, num_results=10):
           print(url)
   
   if __name__ == "__main__":
       query = input("Enter the search query: ")
       google_search(query)