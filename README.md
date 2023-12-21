# Pwnagotchi Screen Inversion Scripts

## Overview
This repository contains two Bash scripts for Pwnagotchi devices equipped with a Waveshare V3 screen and a PiSugar 2 or 3 battery. These scripts enable users to invert the screen colors of their Pwnagotchi, on the go, by pressing or holding a button on the PiSugar battery.

## Prerequisites
- Pwnagotchi device
- Waveshare V3 screen
- PiSugar 2 or 3 battery

## Installation

### Cloning the Repository
First, clone this repository to your Pwnagotchi device in the home directory:
```
cd ~
git clone https://github.com/tPayne0647/pwnagotchi_screen_color_invert.git
cd pwnagotchi_screen_color_invert
```

### Setting File Permissions
After cloning the repository, you need to set the execute permissions for the scripts. Run the following commands:
```
chmod +x invert_colors.sh
chmod +x invert_open.sh
```

### Script Descriptions

1. **invert_colors.sh**: This script inverts the colors of the Pwnagotchi's display.


2. **invert_open.sh**: A helper script to execute `invert_colors.sh` with the necessary permissions.

### Configuring PiSugar
To use these scripts with your PiSugar battery, follow these steps:

1. Access the PiSugar Web GUI on your device.
2. Navigate to the section where you can assign actions to button presses.
3. Assign `/home/pi/invert_open.sh` to the desired button. This will trigger the screen color inversion when the button is pressed.

## Usage
Press the configured button on your PiSugar battery to invert the screen colors of your Pwnagotchi. It will reboot after a few seconds and will come back up with the colors inverted. Press the button again to restore the original colors.

## Notes
- The `invert_colors.sh` script creates a backup of the original `view.py` file before making changes.
- Ensure that your Pwnagotchi and PiSugar are correctly set up.

## Contributing
Feel free to fork this repository and submit pull requests with improvements or fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```markdown
MIT License

Copyright (c) 2023 tPayne0647

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```