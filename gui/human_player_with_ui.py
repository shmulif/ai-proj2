import subprocess
import time
import sys

program1 ='python/connect4.py'
programx = 'gui/test.py'
program2 = 'gui/graphics_program/room_human_player.py'

# Start Program 1
process1 = subprocess.Popen(
    ['python3', '-u', program1],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
)

# Start Program 2
process2 = subprocess.Popen(
    ['python3', '-u', program2],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
)

def consume_initial_lines(process, num_lines_to_ignore=5):
    """
    Function to read and discard the initial lines from a process's stdout.
    Adjust the number of lines to ignore as needed.
    """
    ignored_lines_count = 3
    while True:
        line = process.stdout.readline().strip()
        if not line:
            break  # Stop if the line sis empty (end of output)
        ignored_lines_count += 1
        if ignored_lines_count >= num_lines_to_ignore:
            break  # Stop after ignoring the specified number of lines


# Consume initial lines from Program 2
consume_initial_lines(process2)

def stream_data():
    try:
        program1_output = ""
        end_marker = "): "

        while True:
            char = process1.stdout.read(1)  # Read one character
            if char == "":  # Empty string means no more output
                if process1.poll() is not None:  # Process finished
                    break
            print(f"{char}", end="")
            sys.stdout.flush()  # Ensure immediate output
            program1_output += char
            
            # Check if the end of program1_output matches the end_marker
            if program1_output.endswith(end_marker):
                print("\nEnd of current info reached!")
                break  # Exit the loop if the end_marker is found

        print("we broke out of the loop. yay! we're free!")
        if program1_output:
            print(f"Program 1 Output: \n{program1_output}")
            # Send the full output from Program 1 to Program 2
            process2.stdin.write(program1_output)
            process2.stdin.flush()  # Ensure it gets sent immediately

        # Program 2 responds with just one character (simulate input to Program 1)
        program2_response = process2.stdout.readline().strip()
        if program2_response:
            print(f"Program 2 Response: {program2_response}")

            # Check if process1 is still running before writing
            if process1.poll() is None:  # Ensure process1 is still running
                # Send simulated user input to program1's stdin
                process1.stdin.write(program2_response + "\n")
                process1.stdin.flush()  # Ensure it gets sent immediately
            else:
                print("process1 has finished or failed, cannot write to stdin")

        # Check stderr for any errors from program2
        error_output = process2.stderr.read()
        if error_output:
            print(f"Program 2 Error: {error_output}")

        time.sleep(0.1)  # Small delay to avoid busy waiting

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # Ensure all resources are properly closed when done
        process1.stdin.close()
        process2.stdin.close()
        process1.wait()
        process2.wait()

# Run the streaming function
stream_data()
