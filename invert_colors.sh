#!/bin/bash

# Path to the view.py file
view_file="/usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py"

# Backup the original view.py file
cp "$view_file" "$view_file.bak"

# Edit the view.py file to invert the colors
if grep -q "WHITE = 0xff" "$view_file" && grep -q "BLACK = 0x00" "$view_file"; then
    sed -i 's/WHITE = 0xff/WHITE = 0x00/' "$view_file"
    sed -i 's/BLACK = 0x00/BLACK = 0xff/' "$view_file"
else
    sed -i 's/WHITE = 0x00/WHITE = 0xff/' "$view_file"
    sed -i 's/BLACK = 0xff/BLACK = 0x00/' "$view_file"
fi

touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi
