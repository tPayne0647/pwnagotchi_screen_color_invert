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

# Example usage
# Enable the double press button
enable_response = send_pisugar_command_uds("set_button_enable double 1")
print(enable_response)

# Set the action for the double press button
# Replace the path with the actual path to your script
set_shell_response = send_pisugar_command_uds("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_shell_response)
