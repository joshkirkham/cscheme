#!/usr/bin/python3
  
"""
A program to manage and apply colorschemes for running instances of urxvt
"""

import os
import sys
import subprocess




def parse_color(line):
    """Parses the 6 digit hex color from a line of text"""
    offset = line.rfind("#")
    return line[offset + 1 : offset + 7]




def gen_commands(scheme):
    """ Creates a list of non-human-readable commands for running instances of
    urxvt from a human readable colorscheme file
    """

    colors = []
    try:
        f = open(SCHEMEDIR + "schemes/" + str(scheme), "r")
        for line in f:
            colors.append(parse_color(line))
        f.close()

    except FileNotFoundError:
        print("ERROR: Could not read scheme: " + scheme)

    
    commands = []

    # Foreground and background
    commands.append("\\033]11;#" + str(colors[0]) + "\\007")
    commands.append("\\033]10;#" + str(colors[1]) + "\\007")

    # 16 text colors
    for i in range(2, 18):
        commands.append("\\033]4;" + str(i-2) + ";#" + str(colors[i]) + "\\007")

    return commands




def apply_scheme(commands):
    """ Given a list of commands, it generates a shell script of commands,
    and runs it across all active terminal sessions"""

    script = "#!/bin/sh\n"
    for command in commands:
        script = script + "printf '" + command + "'\n"

    # Create a temporary shell script
    f = open(SCHEMEDIR + "colorscheme.sh", "w+")
    f.write(script)
    f.close()

    print(script)
    os.chmod(SCHEMEDIR + "colorscheme.sh", 777)

    # Run the script on each active terminal
    pts = os.listdir('/dev/pts')
    for each_pts in pts:
        if is_number(each_pts):
            command = SCHEMEDIR + "colorscheme.sh"
            subprocess.call(command + " > /dev/pts/{0}".format(each_pts), shell=True)
    
    # Remove the temporary script
    if (os.path.exists(SCHEMEDIR + "colorscheme.sh")):
        os.remove(SCHEMEDIR + "colorscheme.sh")
    



def is_number(s):
    """Returns true if s is a number"""

    try:
        int(s)
        return True
    except ValueError:
        return False




def template():
    """Prints out a template for a human readable colorscheme file"""

    string = "foreground: #\nbackground: #\n"
    for i in range(0, 16):
        string = string + "color" + str(i) + ": #\n"
    print(string)




def list():
    """Lists the schemes currently in the scheme directory"""

    schemes = os.listdir(SCHEMEDIR + "/schemes/")
    for scheme in schemes:
            print(scheme)




def usage():
    """Prints program usage information"""

    readme = open("README", "r")
    for line in readme:
        print(line, end="")




def run():
    """Gathers input from the command line, and performs the appropriate
    action"""

    if len(sys.argv) == 1:
        usage()

    elif sys.argv[1] == "-h":
        usage()

    elif sys.argv[1] == "list":
        list()

    elif sys.argv[1] == "template":
            template()

    elif sys.argv[1] == "set":
        if len(sys.argv) < 3:
            usage()
        else:
            apply_scheme(gen_commands(sys.argv[2]))




# Run the program
if __name__ == "__main__":
    SCHEMEDIR = "/home/swood/scripts/cscheme/"
    run()

