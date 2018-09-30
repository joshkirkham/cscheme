#!/usr/bin/python3

"""
A program to manage and apply colorschemes for running instances of urxvt
"""

import os
import sys
import subprocess



def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def echo(scheme):
    pts = os.listdir('/dev/pts/')
    for each_pts in pts:
        if is_number(each_pts):
            subprocess.call(scheme + ' > /dev/pts/{0}'.format(each_pts), shell=True)




def gen_colorscheme(commands):

    string = "\#~/bin/bash\n"
    for command in commands:
        string = string + "printf '" + command + "'\n"
    name = input("Name this colorscheme: ")

    directory = "/home/" + USERNAME + "/.config/colorschemes/"
    if not os.path.isdir(directory):
        os.mkdir(directory)

    configfile = open(directory + str(name) + ".sh", "w+")
    configfile.write(string)
    configfile.close()

    print("COLORSCHEME \"" + str(name) + "\" GENERATED")
    


# Generates a list of commands from a colorscheme file
def gen_commands(filepath):
    f = open(filepath, "r")
    lines = f.readlines()

    
    commands.append("\\033]11;#" + str(get_color(lines[0])) + "\\007")
    commands.append("\\033]10;#" + str(get_color(lines[1])) + "\\007")
    
    for i in range(2, 18):
        commands.append("\\033]4;" + str(i) + ";#" + str(get_color(lines[i])) + "\\007")
        
    return commands



#Gets the  6 digit hex color number from a configfile line
def get_color(line):
    offset = line.rfind("#")
    return line[offset+1 : offset + 8]






def list():
    schemes = os.listdir(SCHEMEDIR)
    for scheme in schemes:
        if scheme[-3:] == ".sh":
            print(scheme[0:-3])




def apply(colorscheme):
    colorscheme = colorscheme + ".sh"
    schemes = os.listdir(SCHEMEDIR)
    if colorscheme in schemes:
        pts = os.listdir('/dev/pts/')
        for each_pts in pts:
            if is_number(each_pts):
                subprocess.call(SCHEMEDIR + colorscheme + ' > /dev/pts/{0}'.format(each_pts), shell=True)
        
    else:
        print("ERROR: scheme \"" + colorscheme + "\" not detected")
    
    


def usage():
    readme = open("README", "r")
    for line in readme:
        print(line, end="")



def template():
    string = "#colorscheme name:\n#foreground: #\n#background: #\n"
    for i in range(0, 16):
        string = string + "#color" + str(i) + ": #\n"
    print(string)


def run():
    if len(sys.argv) == 1:
        usage()

    elif sys.argv[1] == "-h":
        usage()
    
    elif sys.argv[1] == "list":
        list()

    elif sys.argv[1] == "generate":
        if len(sys.argv) == 2:
            gen_colorschem(get_color_input())
        elif len(sys.argv) > 2:
            gen_colorscheme(get_color_input(sys.argv[2]))

    elif sys.argv[1] == "set":
        if len(sys.argv) < 3:
            usage()
        else:
            apply(sys.argv[2])

    elif sys.argv[1] == "template":
        template()

        
if __name__ == "__main__":
    SCHEMEDIR = "/home/swood/.config/colorschemes/"
    run()
    

