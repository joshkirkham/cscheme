#!/usr/bin/python3
  
"""
A program to manage and apply colorschemes for running instances of urxvt
"""

import os
import sys
import subprocess




def parse_color(line):
    """Parses the 6 digit hex color or from a line of text"""
    offset = line.rfind("#")
    return line[offset : offset + 7]




def gen_rxvt_commands(settings):
    """Generates a set of rxvt control string commands from a list of settings
    from a colorscheme file"""
    
    commands = []

    # Background
    commands.append("\\033]11;" + str(parse_color(settings[0])) + "\\007")
    commands.append("\\033]708;" + str(parse_color(settings[0])) + "\\007")

    # Foreground
    commands.append("\\033]10;" + str(parse_color(settings[1])) + "\\007")

    # 16 text colors
    for i in range(2, 18):
        commands.append("\\033]4;" + str(i-2) + ";" + str(parse_color(settings[i])) + "\\007")

    return commands




def issue_rxvt_commands(commands):
    """Creates a temporary shell script which echoes commands onto a rxvt terminal
    instance. This script is then executed on all running rxvt instances"""

    script = "#!/bin/sh\n"
    for command in commands:
        script = script + "printf '" + command + "'\n"

    f = open(SCHEMEDIR + "colorscheme.sh", "w+")
    f.write(script)
    f.close()

    #print(script)
    os.chmod(SCHEMEDIR + "colorscheme.sh", 777)

    # Run the script on each active terminal
    # You need to be root to do this
    pts = os.listdir('/dev/pts')
    for each_pts in pts:
        if is_number(each_pts):
            command = SCHEMEDIR + "colorscheme.sh"
            subprocess.call(command + " > /dev/pts/{0}".format(each_pts), shell=True)
    
    # Remove the temporary script
    if (os.path.exists(SCHEMEDIR + "colorscheme.sh")):
        os.remove(SCHEMEDIR + "colorscheme.sh")




def xrdb_merge(xresources):
    """Create a new temporary file, and merge it into the xrdb"""

    print(xresources)
    f = open(SCHEMEDIR + "dynamic-Xresources", "w+")
    f.write(xresources)
    f.close()
    subprocess.call("xrdb -merge " + SCHEMEDIR + "dynamic-Xresources", shell=True)
    os.remove(SCHEMEDIR + "dynamic-Xresources")




def color_i3blocks(color):
    f = open("/home/swood/.scripts/i3blocks/color.py", "w+")
    f.write("color = \"" + color + "\"")
    f.close



def apply_scheme(scheme):
    """ Given the name of a coloscheme, it generates a shell script of commands,
    and runs it across all active terminal sessions """

    # Open the scheme file and read in settings from it
    # Also generate a .Xresources string to be merged later
    settings = []
    xresources = ""
    try:
        f = open(SCHEMEDIR + "schemes/" + str(scheme), "r")
        for line in f:
            settings.append(line)
            xresources += line
        f.close()

        rxvt_commands = gen_rxvt_commands(settings)

    except FileNotFoundError:
        print("ERROR: Could not read scheme: " + scheme)


    # Issue changes to all rxvt terminals 
    issue_rxvt_commands(rxvt_commands)


    # Merge the new settings with the xrdb
    xrdb_merge(xresources)

    #Change the i3blocks settings
    i3b_color = settings[1]
    i3b_color = i3b_color[i3b_color.find("#") : -1]
    color_i3blocks(i3b_color)

    # Restart i3 so that it can pull stuff from the newly updated xrdb
    subprocess.call("i3-msg restart", shell=True)




def is_number(s):
    """Returns true if s is a number"""

    try:
        int(s)
        return True
    except ValueError:
        return False


def set_default(scheme):
    subprocess.call("cp schemes/"  + scheme + " schemes/default", shell=True)



def template():
    """Prints out a template for a human readable colorscheme file"""

    settings = [
            "URxvt.background",
            "URxvt.foreground",
            "URxvt.color0",
            "URxvt.color1",
            "URxvt.color2",
            "URxvt.color3",
            "URxvt.color4",
            "URxvt.color5",
            "URxvt.color6",
            "URxvt.color7",
            "URxvt.color8",
            "URxvt.color9",
            "URxvt.color10",
            "URxvt.color11",
            "URxvt.color12",
            "URxvt.color13",
            "URxvt.color14",
            "URxvt.color15",
            "URxvt.borderColor",
            "i3wm.activeBorder",
            "i3wm.inactiveBorder",
            "i3wm.unfocusBorder",
            "i3wm.directionColor",
            "i3wm.background",
            "i3wm.dmenuNormFG",
            "i3wm.dmenuNormBG",
            "i3wm.dmenuSelectFG",
            "i3wm.dmenuSelectBG",
            ]
            

    for item in settings:
        print(item + ": #")




def list():
    """Lists the schemes currently in the scheme directory"""
    
    schemes = os.listdir(SCHEMEDIR + "/schemes/")
    for scheme in schemes:
            print(scheme)




def usage():
    """Prints program usage information"""

    readme = open("USAGE", "r")
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

    elif sys.argv[1] == "default":
        if len(sys.argv) >= 3:
            set_default(sys.argv[2])

        apply_scheme("default")

    elif sys.argv[1] == "set":
        if len(sys.argv) < 3:
            usage()
        else:
            apply_scheme(sys.argv[2])




# Run the program
if __name__ == "__main__":
    #Note this is the cscheme directory, not the one named "schemes"
    SCHEMEDIR = "/home/swood/.scripts/cscheme/"
    run()
















