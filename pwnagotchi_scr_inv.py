import subprocess

def send_pisugar_command(command, host="10.0.0.2", port=8421):
    # Construct the command to send to the PiSugar server
    full_command = f"echo '{command}' | nc {host} {port}"
    # Execute the command
    result = subprocess.run(
    full_command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=True
)


    # Check for errors
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    else:
        return result.stdout

# # Enable double press
# send_pisugar_command("set_button_enable double 1")

# # Set action for double press
# send_pisugar_command("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")

# Enable and set the double press button
enable_response = send_pisugar_command("set_button_enable double 1")
print(enable_response)

set_shell_response = send_pisugar_command("set_button_shell double sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh")
print(set_shell_response)
