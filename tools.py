
############################  TIVALY SEARCH ####################################################

from datetime import datetime
import requests
import os
import openai

client = openai

# Define the base URL for the API
BASE_URL = "https://api.tavily.com/"
# Example usage
api_key = "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"


def search_tavily(api_key, query, search_depth="basic", include_images=False, include_answer=True,
                  include_raw_content=False, max_results=5, include_domains=None, exclude_domains=None):
    # Define the endpoint
    endpoint = "search"

    # Define the request payload
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "include_images": include_images,
        "include_answer": include_answer,
        "include_raw_content": include_raw_content,
        "max_results": max_results,
        "include_domains": include_domains if include_domains else [],
        "exclude_domains": exclude_domains if exclude_domains else []
    }

    # Make the POST request
    response = requests.post(BASE_URL + endpoint, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print("Error:", response.text)
        return None
   
    
    
    ################################################
    

def research(tool_input: str):
        
    # For advanced search:
    response = search_tavily(api_key, tool_input)
        
    #View Results
    if response:
            # Process the search results
            print("Search Query:", response['query'])
            print("Response Time:", response['response_time'])
            print("Images:", response['images'])
            print("Follow Up Questions:", response['follow_up_questions'])
            print("Results:")
            for result in response['results']:
                #("Title:", result['title'])
                print("Title:", result['title'])
                #st.write("URL:", result['url'])
                print("URL:", result['url'])
                #st.write("Content:", result['content'])
                print("Content:", result['content'])
                #st.write("Score:", result['score'])
                print("Score:", result['score'])
                #st.write("---")
                print("\n")
    print('Done!')
        
        
        # Get the search results as context to pass an LLM
        #response = response['answer']
        # Get content from the search results
    if response['results']:
        response_content = response['results'][0]['content']
        #return response_content
        return "SEARCH RESULTS:", response_content
    else:
        # Handle the case where no results were returned
        response_content = "No results found."
        return response_content



################################## REPORT TOOL ##############################################


def pdfCreate(tool_input: str):
    from xhtml2pdf import pisa
    import markdown2
    # Assuming client is correctly set up and you can make API calls
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a report creator. Given the text, create a report in markdown format."},
            {"role": "user", "content": f"Here is the thing to write a report on: {tool_input}"},
        ],
    )
    
    # Extract the markdown content from the response
    markdown_content = response.choices[0].message.content
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(markdown_content)
    
    # Get current date and time in a specific format
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Define PDF file path with the report name and datetime
    pdf_dir = "pdf"
    
    #if dir does not exist create it
    
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        
    pdf_file_path = os.path.join(pdf_dir, f"ReportName_{current_time}.pdf")
    
    # Convert HTML to PDF
    with open(pdf_file_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    # Check for errors
    if pisa_status.err:
        print('An error occurred while creating the PDF.')
    else:
        print("PDF created successfully.")

    return response




######################### PDF READER ########################################

import PyPDF2

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    # Summarize the text with openai

    return text




