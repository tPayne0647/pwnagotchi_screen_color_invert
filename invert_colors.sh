#!/bin/bash

# invert_colors.sh
# Author: tPayne0647
# License: MIT License
# Contribution: Contributions are welcome!
# Please see https://github.com/tPayne0647/pwnagotchi_screen_color_invert

# This script works by replacing the view.py file with a modified version and
# restarting the pwnagotchi to refresh the colors of the screen.

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Path to the log file
log_file="$SCRIPT_DIR/invert_colors.log"

# Log function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$log_file"
}

log "Script started"

# Path to the view.py file
view_file="/usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py"
log "View file: $view_file"

# Backup file name
backup_count=1
backup_file="${view_file}.bak$backup_count"
log "Backup count: $backup_count"

# Keep incrementing backup_count until we find a free name
while [ -f "$backup_file" ]; do
    backup_count=$((backup_count + 1))
    backup_file="${view_file}.bak$backup_count"
done

# Backup the view.py file and preserve timestamps
cp -p "$view_file" "$backup_file"
log "Backup created: $backup_file"

# Edit the view.py file to invert the colors
if grep -q "WHITE = 0xff" "$view_file" && grep -q "BLACK = 0x00" "$view_file"; then
    sed -i 's/WHITE = 0xff/WHITE = 0x00/' "$view_file"
    sed -i 's/BLACK = 0x00/BLACK = 0xff/' "$view_file"
    log "Inverted colors to WHITE"
else
    sed -i 's/WHITE = 0x00/WHITE = 0xff/' "$view_file"
    sed -i 's/BLACK = 0xff/BLACK = 0x00/' "$view_file"
    log "Inverted colors to BLACK"
fi

# Restart pwnagotchi to refresh screen colors
touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi
log "Pwnagotchi service restarted."

log "Script finished"
