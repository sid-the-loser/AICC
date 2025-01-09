import argparse, os, requests, ovc
from wand.image import Image
from wand.version import formats
import custom_errors as ce

aicc_version = "r1.0.5"

class CustomVersionFlag(argparse.Action):
    def __call__(self, parser, namespace, values, option_string = None):
        print(f"Your version: {aicc_version}")

        online_version = ovc.get_online_version_using_json(
            "https://api.github.com/repos/sid-the-loser/AICC/releases/latest", 
            ["name"], 5)
        
        if online_version is None:
            print("Couldn't check for the latest verison online for some"+
                  " reason :(")
        else:
            if online_version != aicc_version:
                print(f"Online version: {online_version}\nYou can download "+
                      "the latest version of AICC from "+
                      "https://github.com/sid-the-loser/AICC/releases")
            else:
                print("You are currently using the latest version of AICC.")

        parser.exit()

help_text = \
"""
All supported conversion modes:
1. file -> file,
2. link -> file
"""

parser = argparse.ArgumentParser(prog="aicc", 
                              description="All Image Conversion Command"+
                              " (AICC) is for converting any image format to "+
                              f"any other image format. Version: {aicc_version}"
                              , epilog=help_text+"Note: This command makes use"+
                              " of wand module for Python. If you find any "+
                              "bugs in this program, please report it to: "+
                              "https://github.com/sid-the-loser/AICC/issues")

parser.add_argument("from_file", type=str,
                    help="The file or directory or link(must start with"+
                    " \"http://\" or \"https://\") to convert from")
parser.add_argument("to_file", type=str, help="The file or directory to"+
                    " convert to")
parser.add_argument("-v", "--version", action=CustomVersionFlag, nargs=0, help=
                    "Checks the version of the software and compares it with"+
                    " the version available online.")


# Essentially, there are three modes to the conversion depending on the input and
# output details entered:
#
# 1. file -> file
# 2. link -> file
#
# **no** dir -> file (obviously, that's impossible)
# **no** file -> dir (sounds stupid to convert a singular file to a plethora of 
# file extensions, but may add this later if I feel like it)


args = parser.parse_args()

file1 = args.from_file
file2 = args.to_file

file2_dot_split = os.path.abspath(file2).split("\\")[-1].split(".")

if len(file2_dot_split) == 1:
    raise ce.UnsupportedConversion(f"No file extension provided with {file2}")

elif len(formats(file2_dot_split[-1].upper())) == 0:
    raise ce.UnsupportedConversion(f".{file2_dot_split[-1]} file extension is not supported by AICC!"+
                                   " If ImageMagick doesn't support it, AICC doesn't either. Go to"+
                                   " https://imagemagick.org/script/formats.php#supported")

conversion_mode = 1

if os.path.isfile(file1):
    conversion_mode = 1

elif file1.startswith("http://") or file1.startswith("https://"): 
    # since this is the easiest to check for links
    conversion_mode = 2

else:
    raise ce.ModeNotSupported(
        "This mode is not supported yet! Use -h to see all supported"+
        " conversion modes!")

def convert_to(file1: str, file2: str) -> None:
    img = Image(filename=file1)
    img.save(filename=file2)

if conversion_mode == 1: # file -> file
    convert_to(file1, file2)

elif conversion_mode == 2: # link -> file
    res = requests.get(file1)
    with open(".temp_web_img", "wb") as f:
        f.write(res.content)

    convert_to(".temp_web_img", file2)

    open(".temp_web_img", "wb").close()
    os.remove(".temp_web_img")

print("Image saved as {}".format(os.path.abspath(file2)))
print("Done!")
