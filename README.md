# Pwnagotchi w/ Waveshare V3 & PiSugar 2/3 Screen Inversion Script

## Overview
This repository contains a Bash script designed for Pwnagotchi devices equipped with a Waveshare V3 screen and a PiSugar 2 or 3 battery. This script enables users to invert the screen colors of their Pwnagotchi, on the go, by pressing or holding the *custom* button on the PiSugar battery.

## Prerequisites
- Configured Pwnagotchi device
- Waveshare V3 screen  (Needs to be tested on V2)
- PiSugar 2 or 3 battery

## Installation

### Cloning the Repository
First, clone this repository to your Pwnagotchi device in its home directory and navigate to the project directory:
```
cd ~
git clone https://github.com/tPayne0647/pwnagotchi_screen_color_invert.git
cd pwnagotchi_screen_color_invert
```

### Setting File Permissions
After cloning the repository, you need to set the execute permissions by running the following command:
```
chmod +x invert_colors.sh
```

### Configuring PiSugar
To use this script with your PiSugar battery, follow these steps:

1. Access the PiSugar Web GUI on your device ` http://<your raspberry ip>:8421`
2. Navigate to the *Custom Button Function* section where you can assign actions to button presses.
3. Paste `sudo /home/pi/pwnagotchi_screen_color_invert/invert_colors.sh` to the desired button press.

## Usage
Press the configured button on your PiSugar battery to invert the screen colors of your Pwnagotchi. It will restart after a few seconds and will come back up with the colors inverted. Press the button again to restore the original colors.

## Notes
- Ensure that your Pwnagotchi, PiSugar and Waveshare screen are correctly set up before running the scripts.
- The `invert_colors.sh` script creates a backup of the original `view.py` file before making changes.
- The log file can be found in the project directory as `invert_colors.log` for troubleshooting.

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
