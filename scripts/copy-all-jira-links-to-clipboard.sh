#!/bin/zsh

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Copy all open JIRA Links to Clipboard
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔗
# @raycast.packageName Jira Tools

# Documentation:
# @raycast.description Copy a list of formatted JIRA links from the current open tabs in your browser
# @raycast.author Matthew Johnson
# @raycast.authorURL mttjhn.com
#

####################################
# CHANGE THESE VARIABLES FOR SETUP #
####################################
browser="Arc" # Doesn't currently work, see the get-all-tab-urls.scpt to change browser
jiraDomain="mycompany.atlassian.net"

# Start by getting all open URLs from Arc using provided script
urlOutput=$(osascript get-all-tab-urls.scpt)
# Split on the known delimeter "|_|"
urlArray=(${(@s:|_|:)urlOutput})
# Set some global variables for the clipboard
htmlList=""
plaintextList=""
# Loop through all URLs
for url in "${urlArray[@]}"
do
    # Process the URL and prepare list of items for clipboard
    jiraRegex='([A-Z0-9]+-[0-9]+)'
    # Get everything before the query string
    splitUrl=("${(@s/?/)url}")
    cleanUrl=$splitUrl[1]
    # Check if this is a Jira URL, otherwise skip
    if [[ $cleanUrl = *${jiraDomain}/browse* ]]; then
      # Check if there is a Jira tag at the end, otherwise skip
      if [[ $cleanUrl =~ $jiraRegex ]]; then
        jiraIssue=${match[1]}
        html="<a href=\"${cleanUrl}\">${jiraIssue}</a>"
        if ((${#htmlList} > 0 )); then
            htmlList+="<br />"
            plaintextList+="\n"
        fi
        htmlList+=$html
        plaintextList+=$jiraIssue
      fi
    fi
done

# Set the clipboard if we got anything
if ((${#plaintextList} > 0)); then
    hex=`echo -n $htmlList | hexdump -ve '1/1 "%.2x"'`
    osascript -e "set the clipboard to {«class HTML»:«data HTML${hex}», string:\"${plaintextList}\"}"
    echo "✅ All open JIRA links copied to clipboard."
else
    echo "⛔ No JIRA issues found in open tabs."
fi
