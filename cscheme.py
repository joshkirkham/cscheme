import os
import sys
import subprocess

USERNAME = "swood"

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
    

def get_color_input(filepath):
    f = open(filepath, "r")
    colors = f.readlines()
    
    for i in range(0, 16):
        commands.append("\\033]4;" + str(i) + ";#" + str(colors[i]) + "\\007")
        
    commands.append("\\033]11;#" + str(colors[16]) + "\\007")
    commands.append("\\033]10;#" + str(colors[17]) + "\\007")

    return commands


def get_color_input():
    questions = ["0 light black",
            "1 light red",
            "2 light green",
            "3 light yellow",
            "4 light blue",
            "5 light magenta",
            "6 light cyan",
            "7 light gray",
            "8 heavy black",
            "9 heavy red",
            "10 heavy green",
            "11 heavy yellow",
            "12 heavy blue",
            "13 heavy magenta",
            "14 heavy cyan",
            "15 heavy gray",
            "background",
            "foreground"
            ]

    answers = []

    for question in questions:
        answers.append(input(question + ":\t#").upper())

    commands = []

    for i in range(0, 16):
        commands.append("\\033]4;" + str(i) + ";#" + str(answers[i]) + "\\007")
        
    commands.append("\\033]11;#" + str(answers[16]) + "\\007")
    commands.append("\\033]10;#" + str(answers[17]) + "\\007")

    return commands


def list():
    schemes = os.listdir("~/" + USERNAME + "/.config/colorschemes/")
    for scheme in schemes:
        if scheme[-3:] == ".sh":
            print(scheme[0:-3])


def usage():
    print("Usage: cscheme [COMMAND] [TARGET]")
    print("""Commands:
    \tgenerate\tCreates a new colorscheme from a file, or stdin if no target\n\t\t\t is specified
    \tapply\tApplies a named colorscheme
    \tlist\tLists all available colorschemes\n\n""")



def run():
    if len(sys.argv) == 1:
        usage()

    elif sys.argv[1] == "list":
        list()

    elif sys.argv[1] == "generate":
        if len(sys.argv) == 2:
            gen_colorschem(get_color_input())
        elif len(sys.argv) > 2:
            gen_colorscheme(get_color_input(sys.argv[2]))

    elif sys.argv[1] == "apply":
        if len(sys.argv) < 3:
            usage()
        else:
            apply(sys.argv[2])

        
if __name__ == "__main__":
    run()

