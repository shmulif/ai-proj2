import subprocess

# Set the program to input
inputProgram = 'program1.py'

# Run the first program and capture its output
process1 = subprocess.Popen(['python', inputProgram], stdout=subprocess.PIPE)

# Pass the output to the second program
process2 = subprocess.Popen(['python', 'gui/graphics_program/room.py'], stdin=process1.stdout, stdout=subprocess.PIPE)

# Ensure proper closing of pipes
process1.stdout.close()
output = process2.communicate()[0]

print(output.decode())