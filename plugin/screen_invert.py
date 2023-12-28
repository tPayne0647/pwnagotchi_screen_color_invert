# This does not work, enabling this plugin will result in bootlooping. Need help troubleshooting this.

import os
import logging
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.web as web
from client.PiSugarClient import PiSugarClient

logger = logging.getLogger(__name__)

class ScreenInvertPlugin(plugins.Plugin):
    def __init__(self):
        super().__init__()
        self.selected_button = 'double'
        self.menu = ['single', 'double', 'long']
        self.script_path = "/home/pi/pwnagotchi_screen_color_invert/script/invert_colors.sh"
        self.ready = False
        logger.debug("ScreenInvertPlugin initialized.")

    def on_loaded(self):
        logger.debug("on_loaded called for ScreenInvertPlugin.")
        try:
            if os.path.exists(self.script_path) and os.access(self.script_path, os.X_OK):
                logger.info("Script found and is executable.")
                self.ready = True
            else:
                logger.warning("Script not found or not executable at %s", self.script_path)
                self.ready = False
        except Exception as e:
            logger.error("Error in on_loaded: %s", e)

    def apply_button_action(self):
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
        logger.debug("Processing form data: %s", form_data)
        self.selected_button = form_data.get('button_action')
        self.apply_button_action()

    def _log(self, message):
        logging.info("[ScreenInvertPlugin] %s", message)
