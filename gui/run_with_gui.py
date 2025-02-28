import subprocess
import os

# Set the program to input
Program1 = 'python/connect4.py'


# Run the first program and capture its output
process1 = subprocess.Popen(['python3', Program1], stdout=subprocess.PIPE)

# Get the output from program1 (this will be passed as input to program2)
output_program1 = process1.communicate()[0].decode('utf-8').strip()  # Decode to string and remove any extra whitespace
args_for_program2 = output_program1  # Split by whitespace to get a list of arguments

print(args_for_program2)

# Set environment variable to disable output buffering
env = os.environ.copy()
env['PYTHONUNBUFFERED'] = '1'

# Pass the output of program1 as arguments to program2
process2 = subprocess.Popen(
    ['python3', 'gui/graphics_program/room.py', args_for_program2],  # Pass the output as a single argument string
    stdout=subprocess.PIPE,
    env=env  # Set the environment variable to disable buffering
)

# Read and print the output of program2 while it's running
for line in process2.stdout:
    print(line.decode('utf-8').strip())  # Decode to string and remove extra whitespace
