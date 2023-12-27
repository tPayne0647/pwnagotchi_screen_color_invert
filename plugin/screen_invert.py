# This does not work, enabling this plugin will result in bootlooping. Need help troubleshooting this.

import os
import socket
import logging
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.web as web

logger = logging.getLogger(__name__)

class PiSugarClient:
    def __init__(self, socket_path="/tmp/pisugar-server.sock"):
        self.socket_path = socket_path
        logger.debug(f"PiSugarClient initialized with socket path: {self.socket_path}")

    def send_command(self, command):
        logger.debug(f"send_command called with command: {command}")
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                logger.info(f"Connecting to {self.socket_path}")
                sock.connect(self.socket_path)
                logger.debug("Socket connection established.")

                # Clear existing socket data
                sock.settimeout(0.1)
                logger.info("Clearing socket")

                try:
                    while True:
                        data = sock.recv(1024)
                        if not data:
                            break
                        logger.debug(f"Cleared: {data}")
                except socket.timeout:
                    logger.info("Socket clear")

                # Send command
                logger.info(f"Sending: {command}")
                sock.sendall(command.encode() + b'\n')

                # Get response
                response = sock.recv(1024)
                logger.info(f"Received: {response.decode()}")

                return response.decode()
        except socket.error as e:
            logger.error(f"Command failed: {e}")
            return None

class ScreenInvertPlugin(plugins.Plugin):
    def __init__(self):
        super().__init__()
        self.selected_button = 'double'  # Default button
        self.menu = ['single', 'double', 'long']
        self.script_path = "/home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh"
        self.ready = False
        logger.debug("ScreenInvertPlugin initialized.")

    def on_loaded(self):
        try:
            self._log("ScreenInvertPlugin loaded")
            if os.path.exists(self.script_path) and os.access(self.script_path, os.X_OK):
                self._log("Script found and is executable. Ready to execute.")
                self.ready = True
            else:
                self._log(f"Script not found or not executable at {self.script_path}")
                self.ready = False
        except Exception as e:
            self._log(f"Error in on_loaded: {e}")

    def apply_button_action(self):
        logger.debug("Applying button action.")
        pi_sugar_client = PiSugarClient()

        for button in self.menu:
            clear_command = f"set_button_enable {button} 0"
            logger.debug(f"Sending clear command for button {button}")
            pi_sugar_client.send_command(clear_command)

        enable_command = f"set_button_enable {self.selected_button} 1"
        action_command = f"set_button_shell {self.selected_button} sudo {self.script_path}"
        logger.debug(f"Enabling {self.selected_button} button with action command.")

        try:
            pi_sugar_client.send_command(enable_command)
            pi_sugar_client.send_command(action_command)
            self._log(f"Applied action for {self.selected_button} button: {action_command}")
        except Exception as e:
            self._log(f"Error applying button action: {e}")

    def on_webhook(self, path, request):
        logger.debug(f"Webhook called with path: {path}")
        if path == "/screeninvert":
            if request.method == 'GET':
                logger.debug("Handling GET request.")
                return self.render_form()
            elif request.method == 'POST':
                logger.debug("Handling POST request.")
                self.process_form(request.POST)
                return web.HTTPFound('/plugins/screeninvert')
        else:
            logger.warning(f"Unknown path in webhook: {path}")
            return web.Response(status=404, text="Not Found")

    def render_form(self):
        logger.debug("Rendering form.")
        html = '<html><body>'
        html += '<form action="/plugins/screeninvert" method="post">'
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
        logger.debug(f"Processing form data: {form_data}")
        self.selected_button = form_data.get('button_action')
        self.apply_button_action()

    def _log(self, message):
        logging.info(f"[ScreenInvertPlugin] {message}")
