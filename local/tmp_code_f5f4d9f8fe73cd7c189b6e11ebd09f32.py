import shutil

# replace with your source file path
source_file = "C:/Users/robert/Documents/myfile.txt"

# replace with your destination file path
destination_file = "C:/Users/robert/Desktop/myfile.txt"

# use the move function from the shutil module
shutil.move(source_file, destination_file)

print("File moved successfully.")