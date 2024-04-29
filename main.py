import re
from threading import local
import os
from datetime import datetime

#Openai API Key
os.environ["OPENAI_API_KEY"] = "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"


## CERT ISSUE FIX
# pip install python-certifi-win32


# LOCAL IMPORTS
from agents import karen, mitali, brett, robert, code_executor_agent
from tools import research, pdfCreate



###### TIME SETUP ########
today = datetime.now().strftime("%Y-%m-%d")

########## AUTOGEN ######
import tempfile
from autogen import register_function, GroupChat, GroupChatManager
# from autogen import AssistantAgent, UserProxyAgent



## SETUP ###

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# create a local directory to store the code files if it doesn't exist
local_dir = os.path.join(os.getcwd(), "local")





########## REGISTER TOOLS with AGENTS #############


# Additional way to register tools
mitali.register_for_llm(name="research", description="A research tool that accepts a string for an input.")(research)
robert.register_for_execution(name="research")(research)

karen.register_for_llm(name="pdfCreate", description="A pdf creator tool that accepts a string for an input.")(pdfCreate)
robert.register_for_execution(name="pdfCreate")(pdfCreate)



################## GROUP CHAT #############################


# Allows the agents constraints to only talk to certain agents.
allowed_transitions = {
    robert: [brett, mitali, karen],
    mitali: [robert],
    brett: [robert, code_executor_agent],
    karen: [robert], 
}


group_chat_with_introductions = GroupChat(
    agents=[karen, mitali, brett, robert, code_executor_agent],
    allow_repeat_speaker=False,
    speaker_transitions_type="allowed",
    messages=[],
    max_round=20,
    send_introductions=True,
)


group_chat_manager = GroupChatManager(
    groupchat=group_chat_with_introductions,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)





########################## INITIATE CHAT ########################################

message = "I need to build a script to search for something on the internet. I need to create a pdf readme document about the script that was just created. Can you help me with that too?"


chat_result = robert.initiate_chat(
    group_chat_manager,
    message=message,
    summary_method="reflection_with_llm",
)


