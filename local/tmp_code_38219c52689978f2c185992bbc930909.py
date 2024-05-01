import shutil

# replace with your source file path
source_file = "/path/to/source/file.txt"

# replace with your destination file path
destination_file = "/path/to/destination/file.txt"

# use the move function from the shutil module
shutil.move(source_file, destination_file)

print("File moved successfully.")