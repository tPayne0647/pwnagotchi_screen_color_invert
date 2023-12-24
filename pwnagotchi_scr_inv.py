import socket

def send_pisugar_command_uds(command, socket_path="/tmp/pisugar-server.sock"):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(socket_path)
            sock.sendall(command.encode() + b'\n')
            response = sock.recv(1024)
            return response.decode().strip()
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

# Testing

# Enable the double press button
enable_response = send_pisugar_command_uds("set_button_enable double 1")
print(enable_response)

# Set the action for the single press button
set_shell_response = send_pisugar_command_uds("set_button_shell single sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_shell_response)

# Set the action for the double press button
set_shell_response = send_pisugar_command_uds("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_shell_response)

# Set the action for the long press button
set_shell_response = send_pisugar_command_uds("set_button_shell long sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_shell_response)