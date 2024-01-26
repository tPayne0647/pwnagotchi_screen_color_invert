import socket
import logging

# Setting up a logger for logging information and errors
logger = logging.getLogger(__name__)

class PiSugarClient:
    """
    PiSugarClient provides an interface to send commands to the PiSugar
    server via a UNIX socket. It handles connecting to the server, clearing
    the socket, sending commands, and receiving responses.
    """

    def __init__(self, socket_path="/tmp/pisugar-server.sock"):
        """
        Initialize the PiSugarClient with a default socket path.

        :param socket_path: Path to the UNIX socket for PiSugar server.
        """
        self.socket_path = socket_path

    def send_command(self, command):
        """
        Method to send a command to the PiSugar server.

        :param command: The command string to be sent to the server.
        :return: The response from the server as a string, or None if an error occurred.
        """
        try:
            # Creating a UNIX socket
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                logger.info("Connecting to %s", self.socket_path)
                # Connect to the server using the socket path
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
                    # Log when socket is cleared
                    logger.info("Socket clear")

                # Send command
                logger.info("Sending: %s", command)
                sock.sendall(command.encode() + b'\n')

                # Get response
                response = sock.recv(1024)
                logger.info("Received: %s", response.decode())

                return response.decode()
        except socket.error as e:
            # Log any socket errors
            logger.error("Command failed: %s", e)
            return None

# Create an instance of PiSugarClient
client = PiSugarClient()

# TESTING
# The following code is for testing various button press configurations.
# Uncomment the sections you wish to test.

# Disable single press
# print("Disabling single press...")
# response = client.send_command("set_button_enable single 0")
# print(response)

# Enable single press
# print("Enabling single press...")
# response = client.send_command("set_button_enable single 1")
# print(response)

# Set single press action
# print("Setting single press action...")
# response = client.send_command("set_button_shell single sudo /home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh")
# print(response)

# Disable double press
# print("Disabling double press...")
# response = client.send_command("set_button_enable double 0")
# print(response)

# Enable double press
print("Enabling double press...")
response = client.send_command("set_button_enable double 1")
print(response)

# Set double press action
print("Setting double press action...")
response = client.send_command("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh")
print(response)

# Disable long press
# print("Disabling long press...")
# response = client.send_command("set_button_enable long 0")
# print(response)

# Enable long press
# print("Enabling long press...")
# response = client.send_command("set_button_enable long 1")
# print(response)

# Set long press action
# print("Setting long press action...")
# response = client.send_command("set_button_shell long sudo /home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh")
# print(response)
