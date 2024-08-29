import argparse
from PIL import Image
import os
import custom_errors as ce
import requests
import io

help_text = \
"""
All supported conversion modes:

1. file -> file
2. file -> dir *coming soon*
3. dir -> dir *coming soon*
4. link -> file
"""

parser = argparse.ArgumentParser(prog="aicc", 
                              description="All Image Conversion Command (AICC) is for converting any image format to any other image format.",
                              epilog=help_text+"Note: This command makes use of pillow module in Python.")

parser.add_argument("from_file", type=str, help="The file or directory or link(must start with \"http://\" or \"https://\") to convert from")
parser.add_argument("to_file", type=str, help="The file or directory to convert to")
parser.add_argument("extension", type=str, help="The extenstion to convert to")

"""
Essentially, there are four modes to the conversion depending on the input and output details entered:

1. file -> file
2. file -> dir *coming soon*
3. dir -> dir *coming soon*
4. link -> file

**no** dir -> file (obviously, thats impossible)
"""

args = parser.parse_args()

file1 = args.from_file
file2 = args.to_file
file_ext = args.extension

file_ext = f".{file_ext}" if not file_ext.startswith(".") else file_ext

conversion_mode = 1

if os.path.isfile(file1):
    conversion_mode = 1
    """
elif os.path.isfile(file1):
    conversion_mode = 1

    if os.path.isdir(file2):
        conversion_mode = 2

elif os.path.isdir(file1) and os.path.isdir(file2):
    conversion_mode = 3
"""
elif file1.startswith("http://") or file1.startswith("https://"): # since its the easiest to check for (useless optimisation alert!)
    conversion_mode = 4
else:
    raise ce.ModeNotSupported("This mode is not supported yet! Use -h to see all supported conversion modes!")

supported_ext = Image.registered_extensions()

if (file_ext if file_ext.startswith(".") else ".{file_ext}").lower() not in supported_ext:
    temp = f"{file_ext} not supported! Only supported extensions are: "

    for key in supported_ext:
        temp += f"{key} "

    raise ce.UnsupportedConversion(temp)


def split_path_to_list(path: str) -> list:
    list_path = path.split("\\") if path.count("\\") > 0 else path.split("/")
    
    return list_path

def merge_list_to_path(list_path: list) -> str:
    path = ""

    for name in list_path:
        path += name + "\\"

    return path

def convert_to(file1: str, file2: str, ext: str) -> None:
    img = Image.open(file1)
    if not file2.lower().endswith(ext.lower()):
        file2 = f"{file2}{ext}"
    img.save(file2, ext[1:])

if conversion_mode == 1: # file -> file
    convert_to(file1, file2, file_ext)

elif conversion_mode == 2: # file -> dir
    pass

elif conversion_mode == 3: # dir -> dir
    pass

elif conversion_mode == 4: # link -> file
    res = requests.get(file1)
    with open(".temp_web_img", "wb") as f:
        f.write(res.content)

    convert_to(".temp_web_img", file2, file_ext)
    
    open(".temp_web_img", "wb").close()

print("\nImage saved as {}!".format(os.path.abspath(file2)))
print("Done!")