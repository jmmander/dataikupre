import re

def osprinter(osname, gpattern, bpattern):
    good = re.findall(gpattern, osname)
    bad = re.findall(bpattern, osname)
    if good:
        text = (osname + " is being used. ")
        return text
    elif bad:
        text = (osname + " is being used. This is NOT recommended for new installations")
        return text
    else:
        text = (osname + " is being used. This is not currently supported.")
        return text

gpattern = "2017(\.[3-9])"
bpattern = None
osname = "lalalala2017.6"
osprinter(osname, gpattern, bpattern)