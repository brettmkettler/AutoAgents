# Auto Agent Script (Generative AI Laboratory)

This README provides information about the `Auto Agent` script and instructions for setting up and running the code. The script is designed to facilitate interaction with multiple agents that can generate and execute Python code based on user inputs.

## Features

* Setup virtual environment and install dependencies.
* Configure a Streamlit-based user interface to interact with agents.
* Register tools with agents for task planning and execution.
* Facilitate group chats among agents for better task planning.

## Setup

### Requirements

* Python 3.8+
* Virtual environment tools (`venv`)
* Streamlit
* Gevent
* Dotenv

### Setup Instructions

1. **Virtual Environment Setup**
   * Create a virtual environment: `python -m venv AutoAgent`
   * Activate the virtual environment:
     * Windows: `.\AutoAgent\Scripts\Activate`
     * Linux/MacOS: `source AutoAgent/bin/activate`
2. **Install Dependencies**
   * Install the required packages: `pip install -r requirements.txt`
3. **Fix Certificate Issues (if any)**
   * If you encounter certificate issues, install `python-certifi-win32`: `pip install python-certifi-win32`

## Usage

### Configuring Agents

1. **Setup Code Executors**
   * The code executor is set up to execute code in a local environment.
2. **Register Tools with Agents**
   * Different tools are registered with agents to assist in research, PDF creation, and task planning.

### Group Chat Setup

The group chat setup allows for communication among different agents while respecting allowed speaker transitions. This ensures that the right agent receives the message.

### Streamlit UI

* The UI is powered by Streamlit and includes:
  * A header describing the platform.
  * Example use cases to guide users on the capabilities of the platform.
  * Sidebar for user configuration.

### Interaction

* **User Proxy Agent**
  * `TrackableUserProxyAgent` class captures user messages and manages the interactions.
* **Group Chat Manager**
  * `TrackableGroupChatManager` manages the group chat setup and facilitates smooth interaction.

### Executing the Code

* Input a question or command in the Streamlit UI.
* Ensure you have selected the right model and provided the OpenAI API key.
* Agents will process the input and provide responses accordingly.

## Troubleshooting

* Ensure all dependencies are installed correctly.
* Verify the OpenAI API key and model configurations.
* Check for specific error messages in the Streamlit UI and address them accordingly.

## License

This project is licensed under the MIT License.
