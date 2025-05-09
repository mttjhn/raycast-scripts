#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Copy JIRA Link to Clipboard
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔗
# @raycast.packageName Jira Tools

# Documentation:
# @raycast.description Copy a formatted JIRA link from the current open webpage in your browser
# @raycast.author Matthew Johnson
# @raycast.authorURL mttjhn.com

####################################
# CHANGE THESE VARIABLES FOR SETUP #
####################################
browser="Arc"
jiraDomain="mycompany.atlassian.net"

appleScript="tell application \"${browser}\" to return URL of active tab of front window"
urlOutput=$(osascript -e $appleScript)

# Process the URL and set clipboard
jiraRegex='([A-Z0-9]+-[0-9]+)'
# Get everything before the query string
splitUrl=("${(@s/?/)urlOutput}")
cleanUrl=$splitUrl[1]
# Check if this is a Jira URL, otherwise skip
if [[ $cleanUrl = *${jiraDomain}/browse* ]]; then
    echo "Got here."
  if [[ $cleanUrl =~ $jiraRegex ]]; then
    jiraIssue=${match[1]}
    html="<a href=\"${cleanUrl}\">${jiraIssue}</a>"
    hex=`echo -n $html | hexdump -ve '1/1 "%.2x"'`
    osascript -e "set the clipboard to {«class HTML»:«data HTML${hex}», string:\"${jiraIssue}\"}"
    echo "✅ JIRA link copied to clipboard."
  else
    echo "⛔ No JIRA issue found in URL."
  fi
else
  echo "⛔ No JIRA link found."
fi
