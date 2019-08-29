import re
import config
import os

class KV_Store:
    def __init__(self, k: str, v: str):
        this.key = k
        this.value = v

    """
    def check(self, program: str):
        """Check if the prefix of the value is the specified string"""
        return this.key.split(".")[0] == program
    """


class URxvt_Color:
    def __init__(self):
        this.colors = [None] * 16
        this.borderColor = None
        this.background = None
        this.foreground = None

    def apply_kv(self, kv: KV_Store):
        num = re.search('color[01][0-9]', kv.key)
        if num:
            this.colors[int(num.group(0)[5:])] = kv.value
        else:
            try:
                this.__dict__[kv.key] = value
            except KeyError:
                print("Invalid Key for URxvt: " + kv.key)


    def apply_colors(self):
        ESC = "\\033]"
        END = "\\007"
        # Write commands to script file
        # run it for each /dev/pts

        filename = os.path.join(SCHEMEDIR + "urxvt-colors.sh")
        script = open(filename, 'w')
        for i in range(0, len(this.colors):
            script.write(ESC + "4%d;%s" %(i, this.colors[i]) + END) 
        script.write(ESC + "%d;%s" %(11, this.background) + END) 
        script.write(ESC + "%d;%s" %(708, this.background) + END) 
        script.write(ESC + "%d;%s" %(10, this.foreground) + END) 

        script.close()

        os.chmod(filename, 777)
        pts_list = os.listdir('/dev/pts')

        for pts in pts_list:
            if is_number(pts):
                subprocess.call(filename+ " > /dev/pts/{0}".format(pts), shell=True)

        if os.path.exists(filename):
            os.remove(filename)


            
                
            

        


        





