import subprocess
import time

program1 = 'python/connect4.py'
program2 = 'gui/graphics_program/room_human_player.py'

# Start Program 1
process1 = subprocess.Popen(
    ['python3', program1],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
)

# Start Program 2
process2 = subprocess.Popen(
    ['python3', program2],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,
    universal_newlines=True
)

def stream_data():
    try:
        program1_output = ""
        while True:
            line = process1.stdout.readline().split()  # Read one line from program 1
            print(line)
            if line:
                print(f"Read from program1: {line}")  # Debug: Show what we're reading from program1

            if "Enter column (1-7):" in line:  # Stop reading when we hit the expected prompt
                print("we didn't breake out of the loop yet.")
                program1_output += line + "\n"
                break  # Exit the loop after the prompt is received

            if line:  # Only add non-empty lines to the output
                program1_output += line + "\n"  # Add the line to the output buffer
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
