import socket
import time

def send_pisugar_command_uds(command, socket_path="/tmp/pisugar-server.sock"):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            print(f"Connecting to socket: {socket_path}")
            sock.connect(socket_path)

            # Clear any existing data from the socket
            sock.settimeout(0.1)  # Set a short timeout for the receive operation
            print("Clearing any existing data from the socket...")
            try:
                while True:
                    data = sock.recv(1024)
                    if not data:
                        break
                    print(f"Cleared data: {data.decode().strip()}")
            except socket.timeout:
                print("No more data to clear.")

            # Send the command
            print(f"Sending command: {command}")
            sock.sendall(command.encode() + b'\n')
            response = sock.recv(1024)
            print(f"Received response: {response.decode().strip()}")
            return response.decode().strip()
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

# TESTING

# # Enable the single press button
# print("Enabling the single press button...")
# enable_single_response = send_pisugar_command_uds("set_button_enable single 1")
# print(enable_single_response)

# # Set the action for the SINGLE press button
# print("Setting the action for the single press button...")
# set_single_shell_response = send_pisugar_command_uds("set_button_shell single sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(set_single_shell_response)

# Enable the double press button
print("Enabling the double press button...")
enable_double_response = send_pisugar_command_uds("set_button_enable double 1")
print(enable_double_response)

# Set the action for the DOUBLE press button
print("Setting the action for the double press button...")
set_double_shell_response = send_pisugar_command_uds("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_double_shell_response)

# # Enable the long press button
# print("Enabling the long press button...")
# enable_long_response = send_pisugar_command_uds("set_button_enable long 1")
# print(enable_long_response)

# # Set the action for the LONG press button
# print("Setting the action for the long press button...")
# set_long_shell_response = send_pisugar_command_uds("set_button_shell long sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(set_long_shell_response)
