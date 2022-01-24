import os
from PyQt5 import *
from typing import List
import argparse

parser = argparse.ArgumentParser(description="Useful script to create one python file from multiple ones in the same folder")
parser.add_argument("main_filename",metavar="F",type=str,nargs="+")
parser.add_argument("destination_filename",metavar="D",type=str,nargs="+")

args = parser.parse_args()



def get_contents_from_sub_file(filename: str,current_files : List[str],directory: str):
    
    final_file = ""
    
    with open(directory + "/" + filename + ".py", "r",errors="replace") as file:
        file_contents = file.readlines()
    
    for line in file_contents:
        if "from" in line.strip()[:4]:
            file = line.split()[1]
            if file == "one_file":
                continue
            if file in current_files:
                final_file += get_contents_from_sub_file(file,current_files,directory)
            else:
                final_file += line
        else:
            if "create_one_file" in line:
                continue
            final_file += line
    
    final_file += "\n"
    
    current_files.remove(filename)
    
    return final_file


def create_one_file(main_file: str,final_file_name: str,directory : str = os.getcwd()):

    file_names_in_current_folder = [i[:len(i)-3] for i in os.listdir(directory) if i.endswith(".py")]
    final_file = ""
    
    final_file += get_contents_from_sub_file(main_file,file_names_in_current_folder,directory)
    
    with open(directory + "/" + final_file_name + ".py","w",errors="replace") as file:
        file.write(final_file)
        

create_one_file(args.main_filename[0],args.destination_filename[0])