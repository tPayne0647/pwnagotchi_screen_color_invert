# This does not work, enabling this plugin will result in boot looping.
# Need help troubleshooting this.

import os
import sys
import logging
from pathlib import Path
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.web as web

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

logger = logging.getLogger(__name__)

class ScreenInvertPlugin(plugins.Plugin):
    """
    ScreenInvertPlugin is a Pwnagotchi plugin that provides functionality
    for inverting the screen color through button actions on a PiSugar 2/3 external battery.
    """

    def __init__(self):
        """
        Initializes the ScreenInvertPlugin with default settings.
        """
        super().__init__()
        self.selected_button = 'double'
        self.menu = ['single', 'double', 'long']
        self.script_path = Path("/home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh")
        self.ready = False
        logger.debug("ScreenInvertPlugin initialized.")

    def on_loaded(self):
        """
        Called when the plugin is loaded. Checks if the script for inverting
        the screen color exists and is executable.
        """
        logger.debug("on_loaded called for ScreenInvertPlugin.")
        try:
            if self.script_path.exists() and self.script_path.is_file() and os.access(self.script_path, os.X_OK):
                logger.info("Script found and is executable.")
                self.ready = True
            else:
                logger.warning("Script not found or not executable at %s", self.script_path)
                self.ready = False
        except Exception as e:
            logger.error("Error in on_loaded: %s", e)

    def apply_button_action(self):
        """
        Applies the configured action to the selected button on the PiSugar device.
        """
        logger.debug("Applying button action...")
        pi_sugar_client = PiSugarClient()

        for button in self.menu:
            clear_command = f"set_button_enable {button} 0"
            logger.debug("Clearing action for button: %s", button)
            pi_sugar_client.send_command(clear_command)

        enable_command = f"set_button_enable {self.selected_button} 1"
        action_command = f"set_button_shell {self.selected_button} sudo {self.script_path}"
        logger.debug("Setting action for button: %s", self.selected_button)

        try:
            pi_sugar_client.send_command(enable_command)
            pi_sugar_client.send_command(action_command)
            logger.info("Action applied for button: %s", self.selected_button)
        except Exception as e:
            logger.error("Error applying button action: %s", e)

    def on_webhook(self, path, request):
        """
        Handles webhook calls to the plugin.

        :param path: The path of the webhook call.
        :param request: The request object containing details of the HTTP request.
        :return: A web response object.
        """
        logger.debug("Webhook called with path: %s", path)
        if path == "/screen_invert":
            if request.method == 'GET':
                logger.debug("Handling GET request.")
                return self.render_form()
            elif request.method == 'POST':
                logger.debug("Handling POST request.")
                self.process_form(request.POST)
                return web.HTTPFound('/plugins/screen_invert')
        else:
            logger.warning("Unknown path in webhook: %s", path)
            return web.Response(status=404, text="Not Found")

    def render_form(self):
        """
        Renders an HTML form for the user to interact with the plugin.

        :return: A web response object containing the HTML form.
        """
        logger.debug("Rendering form.")
        html = '<html><body>'
        html += '<form action="/plugins/screen_invert" method="post">'
        html += '<select name="button_action">'
        for action in self.menu:
            selected = ' selected' if action == self.selected_button else ''
            html += f'<option value="{action}"{selected}>{action}</option>'
        html += '</select>'
        html += '<input type="submit" value="Apply">'
        html += '</form>'
        html += '</body></html>'
        return web.Response(text=html, content_type='text/html')

    def process_form(self, form_data):
        """
        Processes the form data submitted by the user.

        :param form_data: The data submitted through the form.
        """
        logger.debug("Processing form data: %s", form_data)
        self.selected_button = form_data.get('button_action')
        self.apply_button_action()

    def _log(self, message):
        """
        Logs a message with a specific format for the ScreenInvertPlugin.

        :param message: The message to be logged.
        """
        logging.info("[ScreenInvertPlugin] %s", message)
