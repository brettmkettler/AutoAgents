import re
from threading import local
# from autogen import AssistantAgent, UserProxyAgent
import os
from wsgiref import headers
from click import prompt
from outcome import acapture


#LangSmith API Key
os.environ["LANGCHAIN_API_KEY"] = "ls__e3fe2fb59124490fb2dddca92abcafff"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

#LangSmith Project
os.environ["LANGCHAIN_PROJECT"] = "Multi-Agents Talking"


#Openai API Key
os.environ["OPENAI_API_KEY"] = "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"
from openai import OpenAI
client = OpenAI()




# Ollama
import requests
import json
url = "http://localhost:11434/api/generate"
headers = {
    "Content-Type": "application/json",
}
data = {
    "model": "llama2",
    "prompt": "Create a report on the following text: 'The quick brown fox jumps over the lazy dog.'",
    "stream": False,
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response_test = response.text
data = json.loads(response_test)
actual_response = data["response"]

print(actual_response)



# from datetime import datetime
# ## CERT ISSUE FIX
# # pip install python-certifi-win32



# ### FUNCTIONS ###
# from pydantic import BaseModel, Field
# from typing import Annotated



# class researchInput(BaseModel):
#     a: Annotated[int, Field(description="The item you want to search for.")]

# class reportInput(BaseModel):
#     a: Annotated[int, Field(description="The markdown content to create a report.")]
# ############################  TIVALY SEARCH ####################################################


# import requests


# # Define the base URL for the API
# BASE_URL = "https://api.tavily.com/"
# # Example usage
# api_key = "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"


# def search_tavily(api_key, query, search_depth="basic", include_images=False, include_answer=True,
#                   include_raw_content=False, max_results=5, include_domains=None, exclude_domains=None):
#     # Define the endpoint
#     endpoint = "search"

#     # Define the request payload
#     payload = {
#         "api_key": api_key,
#         "query": query,
#         "search_depth": search_depth,
#         "include_images": include_images,
#         "include_answer": include_answer,
#         "include_raw_content": include_raw_content,
#         "max_results": max_results,
#         "include_domains": include_domains if include_domains else [],
#         "exclude_domains": exclude_domains if exclude_domains else []
#     }

#     # Make the POST request
#     response = requests.post(BASE_URL + endpoint, json=payload)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         return data
#     else:
#         print("Error:", response.text)
#         return None
   
    
    
#     ################################################
    

# def research(input: Annotated[researchInput, "Input to the research tool"]):
        
#     # For advanced search:
#     response = search_tavily(api_key, input.a)
        
#     #View Results
#     if response:
#             # Process the search results
#             print("Search Query:", response['query'])
#             print("Response Time:", response['response_time'])
#             print("Images:", response['images'])
#             print("Follow Up Questions:", response['follow_up_questions'])
#             print("Results:")
#             for result in response['results']:
#                 #("Title:", result['title'])
#                 print("Title:", result['title'])
#                 #st.write("URL:", result['url'])
#                 print("URL:", result['url'])
#                 #st.write("Content:", result['content'])
#                 print("Content:", result['content'])
#                 #st.write("Score:", result['score'])
#                 print("Score:", result['score'])
#                 #st.write("---")
#                 print("\n")
#     print('Done!')
        
        
#         # Get the search results as context to pass an LLM
#         #response = response['answer']
#         # Get content from the search results
#     if response['results']:
#         response_content = response['results'][0]['content']
#         #return response_content
#         return "SEARCH RESULTS:", response_content
#     else:
#         # Handle the case where no results were returned
#         response_content = "No results found."
#         return response_content



# ################################## REPORT TOOL ##############################################


# def pdfCreate(input: Annotated[reportInput, "Input to the report creator tool"]):
#     from xhtml2pdf import pisa
#     import markdown2
#     # Assuming client is correctly set up and you can make API calls
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a report creator. Given the text, create a report in markdown format."},
#             {"role": "user", "content": f"Here is the thing to write a report on: {input.a}"},
#         ],
#     )
    
#     # Extract the markdown content from the response
#     markdown_content = response.choices[0].message.content
    
#     # Convert markdown to HTML
#     html_content = markdown2.markdown(markdown_content)
    
#     # Get current date and time in a specific format
#     current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
#     # Define PDF file path with the report name and datetime
#     pdf_dir = "pdf"
    
#     #if dir does not exist create it
    
#     if not os.path.exists(pdf_dir):
#         os.makedirs(pdf_dir)
        
#     pdf_file_path = os.path.join(pdf_dir, f"ReportName_{current_time}.pdf")
    
#     # Convert HTML to PDF
#     with open(pdf_file_path, "w+b") as pdf_file:
#         pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
#     # Check for errors
#     if pisa_status.err:
#         print('An error occurred while creating the PDF.')
#     else:
#         print("PDF created successfully.")

#     return response




# ######################### PDF READER ########################################

# import PyPDF2

# # Function to extract text from PDF
# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     pdf_reader = PyPDF2.PdfReader(uploaded_file)
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text()
    
#     # Summarize the text with openai

#     return text






# ###### TIME SETUP ########


# today = datetime.now().strftime("%Y-%m-%d")

# ########## SETUP TEMP #########


# import tempfile
# from autogen import ConversableAgent
# from autogen.coding import LocalCommandLineCodeExecutor
# from autogen import register_function

# # Create a temporary directory to store the code files.
# temp_dir = tempfile.TemporaryDirectory()

# # create a local directory to store the code files if it doesn't exist
# local_dir = os.path.join(os.getcwd(), "local")


# # Create a local command line code executor.
# executor = LocalCommandLineCodeExecutor(
#     timeout=10,  # Timeout for each code execution in seconds.
#     work_dir=local_dir,  # Use the temporary directory to store the code files.
    
# )









# ##################################################
# from autogen import GroupChat
# from autogen import GroupChatManager

# # Start the chat
# karen = ConversableAgent(
#     "deductive_reasoning",
#     system_message="""
#     You are the internal dialoge of Robert and you are here to use deductive reasoning to solve problems and you are always looking for ways to improve things and make them more efficient.
#     """,
#     llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
#     human_input_mode="NEVER",  # Never ask for human input.
# )

# joe = ConversableAgent(
#     "curiousity",
#     system_message="""
#     You are the internal dialoge of Robert and you are here to be the curious one and you are always looking for new things to learn and you are always looking for ways to improve things.
#     """,
#     llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
#     human_input_mode="NEVER",  # Never ask for human input.
# )

# brett = ConversableAgent(
#     "brett",
#     system_message="""
#     Your name is Brett and you are always happy and love scripting and coding.
    
#     Your interests are python, life sciences, you are always thinking outside the box, and you are always looking for new ways to solve problems.
#     """,
#     llm_config={"config_list": [{"model": "gpt-3.5-turbo", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
#     human_input_mode="NEVER",  # Never ask for human input.
# )

# robert = ConversableAgent(
#     "robert",
#     system_message="""
#     Your name is Robert and you are the "I" and controller of the group. You will use your brain to think about things and make decisions.
#     """,
#     llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
#     human_input_mode="NEVER",  # Never ask for human input.
# )




# ########## TOOL #############

# # # Register the research
# # register_function(
# #     research,
# #     caller=robert,  # The assistant agent can suggest calls to the calculator.
# #     executor=joe,  # The user proxy agent can execute the calculator calls.
# #     name="research",  # By default, the function name is used as the tool name.
# #     description="A search tool to search things if you need to look up something and search internet about something you want to know more about.",  # A description of the tool.
# # )

# # register_function(
# #     pdfCreate,
# #     caller=robert,  # The assistant agent can suggest calls to the calculator.
# #     executor=karen,  # The user proxy agent can execute the calculator calls.
# #     name="report_creator",  # By default, the function name is used as the tool name.
# #     description="A report creator tool to generate pdf documents.",  # A description of the tool.
# # )

# # allowed_transitions = {
# #     robert: [karen, joe],
# #     # brett: [robert],
# #     karen: [robert],
# #     joe: [robert],
# # }


# group_chat_with_introductions = GroupChat(
#     # agents=[karen, joe, brett, robert, code_writer_agent, code_executor_agent],
#     agents=[karen, joe, robert],
#     #allowed_or_disallowed_speaker_transitions=allowed_transitions,
#     #speaker_transitions_type="allowed",
#     messages=[],
#     max_round=50,
#     #send_introductions=True,
# )


# group_chat_manager = GroupChatManager(
#     groupchat=group_chat_with_introductions,
#     llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
# )


# chat_result = robert.initiate_chat(
#     group_chat_manager,
#     message="""
    
#     Project: america's cup barcelona AI project
    
#     Details: Capgemini, is sponsoring the cup and they have built a LIDAR tool that measures the wind and can predict the wind speed and direction better than the current tools.
#     We also have a "ghost boat" that is a digital twin of the boat that the LIDAR wind is used to find the optimal path for the boat to take.
    
#     I need to come up with use cases to utilize A.I. in this project as the sponsor is looking for innovative ways to use A.I. We can use the LIDAR wind or we could
#     use the ghost boat in the ideas.
    
#     I need to come up with some ideas and think of the best way to use A.I. in this project.
    
#     """,
#     summary_method="reflection_with_llm",
# )

# # result = joe.initiate_chat(karen, message="Cathy what are you doing?!", max_turns=50)