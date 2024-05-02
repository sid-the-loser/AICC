import argparse
from PIL import Image
import os

parser = argparse.ArgumentParser(prog="aicc", 
                              description="All Image Conversion Command (AICC) is for converting any image format to any other image format.",
                              epilog="Note: This command makes use of pillow module in Python.")

parser.add_argument("-c", "--collection", default=None, )
parser.add_argument("file1", help="the file to convert from")
parser.add_argument("file2", help="the file to convert to")

args = parser.parse_args()

supported = Image.registered_extensions()

f1 = args.file1
f2 = args.file2

dir_mode = args.collection

def convert_to(from_: str, to_: str):
    pass

if dir_mode != None:
    for filename in os.listdir(f1):
        print(filename)