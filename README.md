![AICC Logo](https://github.com/sid-the-loser/AICC/blob/main/src/assets/icon.png)
# AICC

A command line tool to convert an image type to another. **AICC** stands for **All Image Conversion Command**.

## How do I use this?

Add the program to your computer's user `PATH` so you can use it from any directory.
Once you've done that, you can run it through the command line.

`aicc <path-to-file/folder that needs conversion> <path-to-file/folder that the converted file should be saved to> <file extension to convert to>`

## What are all the features of this command?

### Current Features
Conversions from:
- `file`      to `file`
- `link`      to `file`
- `directory` to `directory`

### Feature Details
- #### `file` to `file` (devs-only note: `conversion_mode = 1`)
`aicc <path-to-file that needs conversion> <path-to-file that the converted file should be saved to> <file extension to convert to>`

This conversion mode converts a singular file to a different file extension.
- #### `link` to `file` (devs-only note: `conversion_mode = 4`)
`aicc <link to file (must start with "http://" or "https://") that needs conversion> <path-to-file that the converted file should be saved to> <file extension to convert to>`

This conversion mode converts a file from the internet to a different file extension.
- #### `dir` to `dir` (devs-only note: `conversion_mode = 3`)
`aicc <path-to-folder that needs conversion> <path-to-folder that the converted file should be saved to (could be a non-existent folder)> <file extension to convert to>`

This conversion mode converts files from a whole directory into another directory with a different file extension (collectively changing the file extensions of image files to another)

## How do I run this in Python?

1. Clone/Download the git repo
2. Run the `main.py` file using Python3 with all the arguments in place.

Thats it! 

Here is the list of all the necessary modules to run this project:
- `pip install pillow`
- `pip install requests`

## How do I build this script on my own?

 Use [pyinstaller](https://pypi.org/project/pyinstaller/)! I've provided a reference to building the script [here](https://github.com/sid-the-loser/AICC/blob/main/build.sh) for **linux** and [here](https://github.com/sid-the-loser/AICC/blob/main/build.bat) for **windows**.
