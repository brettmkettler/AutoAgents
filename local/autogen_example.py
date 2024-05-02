# filename: autogen_example.py

import autogen.core.autogen as ag

def create_python_script():
    # Create a new auto-gen object
    agent = ag.AutoGen()

    # Add a python function to the script
    agent.add_function("main", [], "print('Hello, World!')")

    # Generate the python script
    python_script = agent.generate()
    
    # Write the script to a file
    with open('autogen_script.py', 'w') as f:
        f.write(python_script)

# Execute the function
create_python_script()