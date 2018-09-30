import os
import sys

def apply(colorscheme):
    colorscheme = colorscheme + ".sh"
    pts = os.listdir('/dev/pts/')
    for each_pts in pts:
        if is_number(each_pts):
            subprocess.call(SCHEMEDIR + colorscheme + ' > /dev/pts/{0}'.format(each_pts), shell=True)
        
    else:
        print("ERROR: scheme \"" + colorscheme + "\" not detected")
