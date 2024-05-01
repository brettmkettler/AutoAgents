import re
from threading import local
import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import gevent
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
from agents import karen, mitali, brett, user_agent, code_executor_agent
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


########## REGISTER TOOLS with AGENTS #############


# Additional way to register tools
mitali.register_for_llm(name="research", description="A research tool that accepts a string for an input.")(research)
user_agent.register_for_execution(name="research")(research)

karen.register_for_llm(name="pdfCreate", description="A pdf creator tool that accepts a string for an input.")(pdfCreate)
user_agent.register_for_execution(name="pdfCreate")(pdfCreate)



################## GROUP CHAT #############################


# Allows the agents constraints to only talk to certain agents.
allowed_transitions = {
    user_agent: [brett, mitali, karen],
    mitali: [user_agent],
    brett: [user_agent, code_executor_agent],
    karen: [user_agent], 
}





################### STREAMLIT UI ############################

st.write("""# Auto Agents""")



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
    user_name = st.text_input("User Name", "User")
    selected_model = st.selectbox("Model", ['gpt-3.5-turbo', 'gpt-4'], index=1)
    selected_key = "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"




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
            agents=[karen, mitali, user_agent, brett, code_executor_agent],
            allow_repeat_speaker=False,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=20,
            send_introductions=True,
        )
        
        group_chat_manager = TrackableGroupChatManager(
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
