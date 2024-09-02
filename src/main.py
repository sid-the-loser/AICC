import argparse
from PIL import Image
import os
import custom_errors as ce
import requests

aicc_version = "r1.0.0"

help_text = \
"""
All supported conversion modes:
file -> file,
link -> file,
dir -> dir.
"""

parser = argparse.ArgumentParser(prog="aicc", 
                              description=f"All Image Conversion Command (AICC) is for converting any image format to any other image format. Version: {aicc_version}",
                              epilog=help_text+"Note: This command makes use of pillow module in Python.")

parser.add_argument("from_file", type=str, help="The file or directory or link(must start with \"http://\" or \"https://\") to convert from")
parser.add_argument("to_file", type=str, help="The file or directory to convert to")
parser.add_argument("extension", type=str, help="The extenstion to convert to")

"""
Essentially, there are three modes to the conversion depending on the input and output details entered:

1. file -> file
3. dir -> dir 
4. link -> file

**no** dir -> file (obviously, thats impossible)
**no** file -> dir (sounds stupid to convert a singular file to a plethura of file extensions, but may add this later if I feel like it)
"""

args = parser.parse_args()

file1 = args.from_file
file2 = args.to_file
file_ext = args.extension

jpg_flag = False

file_ext = f".{file_ext}" if not file_ext.startswith(".") else file_ext

if file_ext.lower() == ".jpg":
    file_ext = ".jpeg"
    jpg_flag = True

conversion_mode = 1

if os.path.isfile(file1):
    conversion_mode = 1

elif os.path.isdir(file1):
    if (not os.path.exists(file2)) or (not os.path.isdir(file2)):
        os.mkdir(file2)

    conversion_mode = 3

elif file1.startswith("http://") or file1.startswith("https://"): # since its the easiest to check for links
    conversion_mode = 4

else:
    raise ce.ModeNotSupported("This mode is not supported yet! Use -h to see all supported conversion modes!")

supported_ext = Image.registered_extensions()

if file_ext.lower() not in supported_ext:
    temp = f"{file_ext} not supported! Only supported extensions are: "

    for key in supported_ext:
        temp += f"{key} "

    raise ce.UnsupportedConversion(temp)


def split_path_to_list(path: str) -> list[str]:
    list_path = path.split("\\") if path.count("\\") > 0 else path.split("/")
    
    return list_path

def merge_list_to_path(list_path: list) -> str:
    path = ""

    for name in list_path:
        if name != "":
            path += name + "\\"

    return path

def get_filename_no_ext_path(filedir):
    filedir_list = split_path_to_list(filedir)
    filename = filedir_list[-1]
    listed_filename = filename.split(".")
    true_fname = ""
    
    for i in range(len(listed_filename)-1):
        true_fname += "."+listed_filename[i]
    
    return true_fname[1:]

def convert_to(file1: str, file2: str, ext: str) -> None:
    global jpg_flag
    img = Image.open(file1)

    if not jpg_flag: # useless optimisation but idc
        pass
    else:
        ext = ".jpg"

    if (not file2.lower().endswith(ext.lower())):
        file2 = f"{file2}{ext}"
    
    img.save(file2, ext[1:] if not jpg_flag else "jpeg")

if conversion_mode == 1: # file -> file
    convert_to(file1, file2, file_ext)

elif conversion_mode == 3: # dir -> dir
    for filename in os.listdir(file1):
        filename = os.path.join(file1, filename)
        if os.path.isfile(filename):
            convert_to(filename, file2+get_filename_no_ext_path(filename), file_ext)

elif conversion_mode == 4: # link -> file
    res = requests.get(file1)
    with open(".temp_web_img", "wb") as f:
        f.write(res.content)

    convert_to(".temp_web_img", file2, file_ext)
    
    open(".temp_web_img", "wb").close()

print("\nImage saved as {}".format(os.path.abspath(file2)))
print("Done!")