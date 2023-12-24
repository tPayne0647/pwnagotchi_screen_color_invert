import socket
import time

def send_pisugar_command_uds(command, socket_path="/tmp/pisugar-server.sock"):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(socket_path)

            # Clear any existing data from the socket
            sock.settimeout(0.1)  # Set a short timeout for the receive operation
            try:
                while True:
                    data = sock.recv(1024)
                    if not data:
                        break
            except socket.timeout:
                pass  # Ignore timeout errors, as they are expected

            # Send the command
            sock.sendall(command.encode() + b'\n')
            response = sock.recv(1024)
            return response.decode().strip()
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

# TESTING

# # Enable the single press button
# enable_single_response = send_pisugar_command_uds("set_button_enable single 1")
# print(enable_single_response)

# # Set the action for the SINGLE press button
# set_single_shell_response = send_pisugar_command_uds("set_button_shell single sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(set_single_shell_response)

# Enable the double press button
enable_double_response = send_pisugar_command_uds("set_button_enable double 1")
print(enable_double_response)

# Set the action for the DOUBLE press button
set_double_shell_response = send_pisugar_command_uds("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_double_shell_response)

# # Enable the long press button
# enable_long_response = send_pisugar_command_uds("set_button_enable long 1")
# print(enable_long_response)

# # Set the action for the LONG press button
# set_long_shell_response = send_pisugar_command_uds("set_button_shell long sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(set_long_shell_response)
