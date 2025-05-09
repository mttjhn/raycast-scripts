# raycast-scripts
A collection of scripts I use with the Raycast tool to automate regular tasks on my Mac. See below for documentation of the scripts in this repository:

## path-swapper ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/scripts/path-swapper.py))
This script helps to "translate" from Windows UNC paths to macOS-friendly paths, and vice-versa. I recently ported this from my Alfred workflow of the same name, but this script has a much simpler set of functions. The script looks at your clipboard for a file path that is a network location and converts it to a Windows UNC path or macOS-friendly path (e.g. SMB or a mounted volume path if possible) and updates the clipboard with the result. See below for a demo:
![Pathswapper Example Screencast](https://raw.githubusercontent.com/mttjhn/raycast-scripts/master/media/PathswapperDemo.gif)

## strip-formatting-paste ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/scripts/strip-formatting-and-paste.applescript))
I ported this general idea from another Alfred workflow that I found, because I often want to paste as plain text and can't remember the keyboard shortcut. This uses AppleScript to do the keyboard shortcut on my behalf.

## copy-jira-link-to-clipboard ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/scripts/copy-jira-link-to-clipboard.sh))
This is a handy script for Jira users; it will look at your currently open browser window and attempt to get the URL of the open tab. If it's a Jira issue, it will try and copy a "clickable" URL to the clipboard with just the Jira issue number as the text.

*Setup Note:* you will need to edit the script and replace the following variables:
* `browser`: this is either "Arc" or "Google Chrome". AppleScript will need it to tell the browser
* `jiraDomain`: this is the root URL of your Jira site that you're using, without http/https on the front (e.g. `mycompany.atlassian.net`).

## copy-all-jira-links-to-clipboard ([Download](https://raw.github.com/mttjhn/raycast-scripts/master/scripts/copy-all-jira-links-to-clipboard.sh))
This is almost exactly like *copy-jira-link-to-clipboard* (above), but it looks for any Jira links in all of tabs on the open browser window. Note that this script requries another script to be present in your scripts directory: [`get-all-tab-urls.scpt`](https://raw.github.com/mttjhn/raycast-scripts/master/scripts/get-all-tab-urls.scpt). It also assumes you're using Arc as your browser... but some quick modifications to that script would likely make it work in Google Chrome.

*Setup Note:* you will need to edit the script and replace the following variables:
* `browser`: this doesn't actually do anything. As noted above, modify the get-all-tab-urls.scpt file to change the browser.
* `jira-domain`: this is the root URL of your Jira site that you're using, without http/https on the front (e.g. `mycompany.atlassian.net`).
