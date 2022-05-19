# raycast-scripts
A collection of scripts I use with the Raycast tool to automate regular tasks on my Mac. See below for documentation of the scripts in this repository:

## path-swapper ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/path-swapper.py))
This script helps to "translate" from Windows UNC paths to macOS-friendly paths, and vice-versa. I recently ported this from my Alfred workflow of the same name, but this script has a much simpler set of functions. The script looks at your clipboard for a file path that is a network location and converts it to a Windows UNC path or macOS-friendly path (e.g. SMB or a mounted volume path if possible) and updates the clipboard with the result. See below for a demo:
![Pathswapper Example Screencast](https://raw.githubusercontent.com/mttjhn/raycast-scripts/master/media/PathswapperDemo.gif)

## strip-formatting-paste ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/strip-formatting-and-paste.applescript))
I ported this general idea from another Alfred workflow that I found, because I often want to paste as plain text and can't remember the keyboard shortcut. This uses AppleScript to do the keyboard shortcut on my behalf.
