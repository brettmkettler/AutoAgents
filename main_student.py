import re
from threading import local
# from autogen import AssistantAgent, UserProxyAgent
import os


#LangSmith API Key
os.environ["LANGCHAIN_API_KEY"] = "ls__e3fe2fb59124490fb2dddca92abcafff"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

#LangSmith Project
os.environ["LANGCHAIN_PROJECT"] = "Multi-Agents Talking"


#Openai API Key
os.environ["OPENAI_API_KEY"] = "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"
from openai import OpenAI
client = OpenAI()

from datetime import datetime
## CERT ISSUE FIX
# pip install python-certifi-win32



### FUNCTIONS ###
from pydantic import BaseModel, Field
from typing import Annotated



class researchInput(BaseModel):
    a: Annotated[int, Field(description="The item you want to search for.")]

class reportInput(BaseModel):
    a: Annotated[int, Field(description="The markdown content to create a report.")]
############################  TIVALY SEARCH ####################################################


import requests


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
    

def research(input: Annotated[researchInput, "Input to the research tool"]):
        
    # For advanced search:
    response = search_tavily(api_key, input.a)
        
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


def pdfCreate(input: Annotated[reportInput, "Input to the report creator tool"]):
    from xhtml2pdf import pisa
    import markdown2
    # Assuming client is correctly set up and you can make API calls
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a report creator. Given the text, create a report in markdown format."},
            {"role": "user", "content": f"Here is the thing to write a report on: {input.a}"},
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



# import fitz  # Import PyMuPDF

# def extract_text(pdf_path):
#     doc = fitz.open(pdf_path)
#     texts = []
#     for page in doc:
#         text = page.get_text("text")
#         texts.append(text)
#     doc.close()
#     return texts

# pdf_texts = extract_text("pdfmicro.pdf")


# def preprocess_text(text):
#     return text.strip().lower()

# texts = [preprocess_text(text) for text in pdf_texts]

# import openai

# openai.api_key = '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'

# def get_embeddings(texts):
#     # OpenAI recommends splitting large texts into chunks that are manageable
#     # Also, ensure you handle rate limits and potential API errors
#     embeddings = []
#     for text in texts:
#         response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
#         embeddings.append(response['data']['embedding'])
#     return embeddings

# embeddings = get_embeddings(texts)






###### TIME SETUP ########


today = datetime.now().strftime("%Y-%m-%d")

########## SETUP TEMP #########


import tempfile
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import register_function

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# create a local directory to store the code files if it doesn't exist
local_dir = os.path.join(os.getcwd(), "local")


# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=local_dir,  # Use the temporary directory to store the code files.
    
)









##################################################
from autogen import GroupChat
from autogen import GroupChatManager

# Start the chat
kimber = ConversableAgent(
    "student",
    system_message="""
    Your name is Kimber, You are the student and you are going to test questions.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

brett = ConversableAgent(
    "test_answerer",
    system_message="""
    Your name is Brett, You are the test answerer and you are going to answer the questions on the test for Kimber. You have a specialty in microeconomics. 
    
    Reference the following resources for the test:
    principles of microeconomics
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

fact_checker = ConversableAgent(
    "fact_checker",
    system_message="""
    Your job is to fact check the answers that Brett provides to Kimber. You will be responsible for verifying the accuracy of the answers provided by Brett.
    
    Reference the following resources for the test:
    principles of microeconomics
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)




########## TOOL #############

# # Register the research
register_function(
    research,
    caller=kimber,  # The assistant agent can suggest calls to the calculator.
    executor=brett,  # The user proxy agent can execute the calculator calls.
    name="research",  # By default, the function name is used as the tool name.
    description="A search tool to search things if you need to look up something and search internet about something you want to know more about.",  # A description of the tool.
)




group_chat_with_introductions = GroupChat(
    # agents=[karen, joe, brett, robert, code_writer_agent, code_executor_agent],
    agents=[kimber, brett, fact_checker],
    speaker_transitions_type="allowed",
    messages=[],
    max_round=5,
    send_introductions=True,
)


group_chat_manager = GroupChatManager(
    groupchat=group_chat_with_introductions,
    llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
)


chat_result = kimber.initiate_chat(
    group_chat_manager,
    message="""
    
    Research a local movie theater in the area you live in and visit the theatre website and find out allthe different types of prices by time of day and day of week and whether they offer kids military or senior discounts.
    
    Make sure to provide the name of the theater and the website address.
    
    """,
    
    summary_method="reflection_with_llm",
)

# result = joe.initiate_chat(karen, message="Cathy what are you doing?!", max_turns=50)