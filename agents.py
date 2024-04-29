
import os
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# create a local directory to store the code files if it doesn't exist
local_dir = os.path.join(os.getcwd(), "local")

########## CODE WRITER ###############

code_writer_system_message = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply 'TERMINATE' in the end when everything is done.
"""

code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    code_execution_config=False,  # Turn off code execution for this agent.
)

##################################################

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=local_dir,  # Use the temporary directory to store the code files.
    
)

# Start the chat
karen = ConversableAgent(
    "karen",
    system_message="""
    Your name is Karen and you are the report generator. You can write very detailed reports and can help with creating reports. You have access to the pdf_report_creator tool to create pdf reports.
    """,
    llm_config={"config_list": [{"model": "gpt-3.5-turbo", "temperature": 0.5, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

mitali = ConversableAgent(
    "Mitali",
    system_message="""
    Your name is Mitali and you love to research things and find out more about things and are very ethical. You do not script things.
    """,
    llm_config={"config_list": [{"model": "gpt-3.5-turbo", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

brett = ConversableAgent(
    "Brett",
    system_message=code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

robert = ConversableAgent(
    "robert",
    system_message="""
    Your name is Robert and you are the Executive Vice President. 
    You are the boss of everyone and you are always in control.
    
    Mitali is a researcher and can ask him to research things for you.
    Brett is the scripter and developer and can ask him to create scripts for you.
    Karen is the report generator and can ask her to create reports for you.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.3, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="NEVER",  # Always take human input for this agent for safety.
)

