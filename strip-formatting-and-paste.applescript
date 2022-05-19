#!/usr/bin/osascript

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Strip Formatting and Paste
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📋
# @raycast.packageName Text Tools

# Documentation:
# @raycast.description Use the system keyboard shortcut to paste without formatting
# @raycast.author Matthew Johnson
# @raycast.authorURL mttjhn.com

tell application "System Events"
    keystroke "v" using {command down, option down, shift down}
    log "Pasting text without formatting... 📋"
end tell
