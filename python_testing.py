import socket
import logging

logger = logging.getLogger(__name__)

class PiSugarClient:
    def __init__(self, socket_path="/tmp/pisugar-server.sock"):
        self.socket_path = socket_path

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                logger.info("Connecting to %s", self.socket_path)
                sock.connect(self.socket_path)

                # Clear existing socket data
                sock.settimeout(0.1)
                logger.info("Clearing socket")

                try:
                    while True:
                        data = sock.recv(1024)
                        if not data:
                            break
                        logger.debug("Cleared: %s", data)
                except socket.timeout:
                    logger.info("Socket clear")

                # Send command
                logger.info("Sending: %s", command)
                sock.sendall(command.encode() + b'\n')

                # Get response
                response = sock.recv(1024)
                logger.info("Received: %s", response.decode())

                return response.decode()
        except socket.error as e:
            logger.error("Command failed: %s", e)
            return None

client = PiSugarClient()

# TESTING

# # Disable single press
print("Disabling single press...")
response = client.send_command("set_button_enable single 0")
print(response)

# # Enable single press
# print("Enabling single press...")
# response = client.send_command("set_button_enable single 1")
# print(response)

# # Set single press action
# print("Setting single press action...")
# response = client.send_command("set_button_shell single sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(response)

# # Disable double press
print("Disabling double press...")
response = client.send_command("set_button_enable double 0")
print(response)

# Enable double press
print("Enabling double press...")
response = client.send_command("set_button_enable double 1")
print(response)

# Set double press action
print("Setting double press action...")
response = client.send_command("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(response)

# # Disable long press
print("Disabling long press...")
response = client.send_command("set_button_enable long 0")
print(response)

# # Enable long press
# print("Enabling long press...")
# response = client.send_command("set_button_enable long 1")
# print(response)

# # Set long press action
# print("Setting long press action...")
# response = client.send_command("set_button_shell long sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
# print(response)
