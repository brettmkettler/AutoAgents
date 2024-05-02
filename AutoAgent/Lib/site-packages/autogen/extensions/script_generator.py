# filename: script_generator.py

def create_python_script():
    # Define the content of the new Python script
    script_content = """
def hello_world():
    print('Hello, World!')

if __name__ == '__main__':
    hello_world()
"""

    # Write the content to a new Python script file
    with open('generated_script.py', 'w') as file:
        file.write(script_content)

# Call the function to create the script
create_python_script()