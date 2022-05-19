#!/usr/bin/env python3

import subprocess
import os
import urllib

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Path Swapper
# @raycast.mode silent

# Optional parameters:
# @raycast.icon ♻️
# @raycast.packageName PathSwapper

# Documentation:
# @raycast.description Swap paths between Windows and macOS paths
# @raycast.author Matthew Johnson
# @raycast.authorURL mttjhn.com


# This function gets the current clipboard contents (in text)
def getClipboard():
    p = subprocess.Popen(["pbpaste"], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read()
    return data.decode("ascii")


def setClipboard(data):
    subprocess.run("pbcopy", universal_newlines=True, input=data)


def getNetworkFromMount(mountPath):
    df = subprocess.Popen(["df", mountPath], stdout=subprocess.PIPE)
    outputLine = df.stdout.readlines()[1]
    outputLine = outputLine.decode("ascii")
    uncPath = outputLine.split()[0]
    # Remove the user login info from the front
    serverPath = uncPath.split("@")[1].lower()
    return serverPath


def getMountFromNetwork(networkPath):
    df = subprocess.Popen(["df", "-T", "smbfs"], stdout=subprocess.PIPE)
    for m in df.stdout.readlines():
        mount = m.decode("ascii")
        # Skip the header line when parsing STDOUT
        if not mount.startswith("Filesystem"):
            uncPath = mount.split()[0]
            mountLoc = mount.split()[8]
            serverPath = uncPath.split("@")[1].lower()
            if serverPath.lower() == networkPath.lower():
                return mountLoc
            else:
                networkSplit = networkPath.split("/")
                if len(networkSplit) == 2:
                    if (
                        networkSplit[0].lower() in serverPath.lower()
                        and networkSplit[1].lower() in serverPath.lower()
                    ):
                        return mountLoc


# This function converts Windows to SMB paths
def convertToSmb(winPath):
    # Assumes that winPath is something like '\\server\share'
    return "smb:" + flipForward(winPath)


# This function converts Windows to mounted Volumes
def convertToVolume(path, isSmb):
    output = None
    if isSmb:
        # Assumes that path is a SMB path
        splitPath = path[6:].split("/")
        server = splitPath[0]
        share = splitPath[1]
        networkPath = server + "/" + share
        mountPath = getMountFromNetwork(networkPath)
        # Check to see if the path is not null AND is mounted
        if mountPath and os.path.exists(mountPath):
            # Simplistic version here...
            output = flipForward(path[6:].replace(networkPath, mountPath))
    else:
        # Assumes that path is a Windows path, something like '\\server\share'
        # Start by parsing out the server and share
        splitPath = path[2:].split("\\")
        server = splitPath[0]
        share = splitPath[1]
        networkPath = server + "/" + share
        mountPath = getMountFromNetwork(networkPath)
        # Check to see if the path is not null AND is mounted
        if mountPath and os.path.exists(mountPath):
            # Simplistic version here...
            output = flipForward(path[2:]).replace(networkPath, mountPath)

    return output


# This function converts from Mac to Windows Links
def convertToWindows(macPath, isSmb):
    output = None

    if isSmb:
        # Assumes we have a fully-qualified SMB link
        output = flipBack(macPath.replace("smb://", "//"))
    else:
        # Assumes we're starting with a classic /Volumes/ link
        splitPath = macPath[1:].split("/")
        share = splitPath[1].strip()
        mountLoc = "/" + splitPath[0] + "/" + share
        replace = None
        networkMnt = getNetworkFromMount(mountLoc + "/")
        replace = networkMnt

        if replace is not None:
            output = flipBack("\\\\" + macPath.replace(mountLoc, replace))
    return output


# This function flips slashes to forward-slashes
def flipForward(input):
    return input.replace("\\", "/")


# This function flips slashes to back-slashes
def flipBack(input):
    return input.replace("/", "\\")


# Swap clipboard method - takes input and does the correct thing
def swapClipboard():
    clipValue = getClipboard()

    if clipValue is not None:
        # Start by trimming whitespace
        clipValue = clipValue.strip()

        # Then, let's check the contents to see what we have
        # Check first for file:// and flip it if needed
        if clipValue[:7] == "file://":
            clipValue = urllib.unquote(clipValue).decode("utf8")
            clipValue = flipBack(clipValue.replace("file:", ""))
        # Now, let's go through the contents!
        if clipValue[:2] == "\\\\":
            # We likely have a windows path!
            volPath = convertToVolume(clipValue, False)
            if volPath is not None:
                setClipboard(volPath)
                print("✅ Converted Windows path to mounted macOS volume path")
            else:
                smbPath = convertToSmb(clipValue)
                setClipboard(smbPath)
                print("✅ Converted Windows path to macOS path")
            return
        elif clipValue is not None and clipValue[:6] == "smb://":
            # We likely have a smb:// path
            # Check for windows path to copy
            winPath = convertToWindows(clipValue, True)
            if winPath is not None:
                # Copy winPath to the clipboard
                setClipboard(winPath)
                print("✅ Converted from macOS SMB path to Windows UNC")
                return
        elif clipValue[:7] == "file://":
            # We have some form of File path. Let's see what we can do...
            print("⚠️ Found a file:// path. Don't know what to do here")
            return
        elif clipValue is not None and clipValue[:1] == "/":
            # We likely have a Mac Path
            # Check for mounted volumes here
            if clipValue[:9] == "/Volumes/":
                winPath = convertToWindows(clipValue, False)
                if winPath is not None:
                    # Copy windows path to clipboard
                    setClipboard(winPath)
                    print("✅ Converted from macOS path to Windows UNC")
                    return
            print("⚠️ Clipboard doesn't appear to contain a network path")
        else:
            print("⚠️ Clipboard doesn't appear to contain a network path")


swapClipboard()
