#!/bin/bash

# Path to the view.py file
view_file="/usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py"

# Backup file name
backup_count=1
backup_file="${view_file}.bak$backup_count"

# Keep incrementing backup_count until we find a free name
while [ -f "$backup_file" ]; do
    backup_count=$((backup_count + 1))
    backup_file="${view_file}.bak$backup_count"
done

# Backup the file and preserve timestamps
cp -p "$view_file" "$backup_file"

# Edit the view.py file to invert the colors
if grep -q "WHITE = 0xff" "$view_file" && grep -q "BLACK = 0x00" "$view_file"; then
    sed -i 's/WHITE = 0xff/WHITE = 0x00/' "$view_file"
    sed -i 's/BLACK = 0x00/BLACK = 0xff/' "$view_file"
else
    sed -i 's/WHITE = 0x00/WHITE = 0xff/' "$view_file"
    sed -i 's/BLACK = 0xff/BLACK = 0x00/' "$view_file"
fi

# Restart to refresh screen colors
touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi
