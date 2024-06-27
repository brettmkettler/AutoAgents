import re
from threading import local
import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import gevent
from typing import Callable, Dict, Literal, Optional, Union
from typing_extensions import Annotated
from autogen import Cache
from autogen.coding import LocalCommandLineCodeExecutor

load_dotenv()


######################################################
# SETUP:
#
# Setup venv and install the requirements
# 1. Create a virtual environment -> python -m venv AutoAgent
# 2. Activate the virtual environment -> .\AutoAgent\Scripts\Activate
# 3. Install the requirements -> pip install -r requirements.txt
# 
#
#




## CERT ISSUE FIX
# pip install python-certifi-win32


# LOCAL IMPORTS
from agents import karen, mitali, brett, user_agent, code_executor_agent, planner
from tools import research, pdfCreate



###### TIME SETUP ########
today = datetime.now().strftime("%Y-%m-%d")

########## AUTOGEN ######
import tempfile
from autogen import register_function, GroupChat, GroupChatManager, UserProxyAgent, AssistantAgent
# from autogen import AssistantAgent, UserProxyAgent



## SETUP ###

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# create a local directory to store the code files if it doesn't exist
local_dir = os.path.join(os.getcwd(), "local")


# Create the directory if it does not exist.
if not os.path.exists(local_dir):
    os.makedirs(local_dir)

# List all files in the directory.
files = os.listdir(local_dir)






def task_planner(question: Annotated[str, "Question to ask the planner."]) -> str:
    with Cache.disk(cache_seed=4) as cache:
        user_agent.initiate_chat(planner, message=question, max_turns=1, cache=cache)
    # return the last message received from the planner
    return user_agent.last_message()["content"]



# Setting up code executor.
os.makedirs("planning", exist_ok=True)
# Use DockerCommandLineCodeExecutor to run code in a docker container.
# code_executor = DockerCommandLineCodeExecutor(work_dir="planning")
code_executor = LocalCommandLineCodeExecutor(work_dir="planning")






########## REGISTER TOOLS with AGENTS #############


# Additional way to register tools
mitali.register_for_llm(name="research", description="A research tool that accepts a string for an input.")(research)
user_agent.register_for_execution(name="research")(research)

karen.register_for_llm(name="pdfCreate", description="A pdf creator tool that accepts a string for an input.")(pdfCreate)
user_agent.register_for_execution(name="pdfCreate")(pdfCreate)

# planner.register_for_llm(name="task_planner", description="A task planner than can help you with decomposing a complex task into sub-tasks.")(task_planner)
# user_agent.register_for_execution(name="task_planner")(task_planner)



################## GROUP CHAT #############################


# Allows the agents constraints to only talk to certain agents.
allowed_transitions = {
    user_agent: [brett, mitali, karen, user_agent],
    mitali: [user_agent],
    brett: [user_agent, code_executor_agent],
    karen: [user_agent], 
}





################### STREAMLIT UI ############################

st.write("""# Auto Agents""")

st.write(""" A conversational AI platform that allows you to interact with multiple agents to create and execute code.""")

st.write("""## Example Use Cases""")
st.write("""1. Write a python code to display the stock price of Capgemini.""")
st.write("""2. Create a python code to display the weather of Paris.""")

class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class TrackableGroupChatManager(GroupChatManager):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)



selected_model = None





with st.sidebar:
    st.header("Configuration")
    st.write("Must use GPT4 model for now.")
    user_name = st.text_input("User Name", "User")
    selected_model = st.selectbox("Model", ['gpt-3.5-turbo', 'gpt-4'], index=1)
    
    #selected_key = st.text_input("OpenAI API Key", "KeyGoesHere")
    
    selected_key = os.environ["OPENAI_API_KEY"]




with st.container():
    # for message in st.session_state["messages"]:
    #    st.markdown(message)

    user_input = st.chat_input("Type something...")
    if user_input:
        if not selected_key or not selected_model:
            st.warning(
                'You must provide valid OpenAI API key and choose preferred model', icon="⚠️")
            st.stop()

        llm_config = {
            "request_timeout": 600,
            "config_list": [
                {
                    "model": selected_model,
                    "api_key": selected_key
                }
            ]
        }
        
        # create a UserProxyAgent instance named "user"
        user_proxy = TrackableUserProxyAgent(
            name=user_name, human_input_mode="NEVER", llm_config=llm_config)

        
        group_chat_with_introductions = GroupChat(
            agents=[planner, karen, mitali, user_agent, brett, code_executor_agent],
            allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=20,
            send_introductions=True,
        )
        
        group_chat_manager = TrackableGroupChatManager(
            system_message=""""You can use the task planner to decompose a complex task into sub-tasks. "
            Make sure your follow through the sub-tasks. 
            When needed, write Python code in markdown blocks, and I will execute them.
            Give the user a final solution at the end.
            Return TERMINATE only if the sub-tasks are completed.""",
            groupchat=group_chat_with_introductions,
            llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )
        
        
        
        def initiate_chat_sync():
            user_agent.initiate_chat(
                group_chat_manager,
                message=user_input,
                summary_method="reflection_with_llm"
            )

        # Run the initiate_chat_sync in a greenlet
        gevent.spawn(initiate_chat_sync).join()                                                                         
