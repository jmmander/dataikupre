if "Red Hat" in osname:
    splitname = re.split('(\d+)', osname)
    print(splitname)
    if splitname[1] > 7.29 and splitname[1] < 8:
        text = "Nice work! You are using " + osname
        print(colour('green', text))
        replist.append(text)
    elif splitname[1] > 6.79 and splitname[1] < 7:
        text = "Uh oh, you are using " + osname + ". This is not recommended for new installs"
        print(colour('blue', text))
        replist.append(text)
    else:
        text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
        print(colour('red', text))
        replist.append(text)
elif "CentOS" in osname:
    splitname = re.split('(\d+)', osname)
    if splitname[1] > 7.29 and splitname[1] < 8:
        text = "Nice work! You are using " + osname
        print(colour('green', text))
        replist.append(text)
    elif splitname[1] > 6.79 and splitname[1] < 7:
        text = "Uh oh, you are using " + osname + ". This is not recommended for new installs"
        print(colour('blue', text))
        replist.append(text)
    else:
        text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
        print(colour('red', text))
        replist.append(text)
elif "Ubuntu" in osname:
    if "LTS" in osname:
        if "16.04" or "18.04" in osname:
            text = "Nice work! You are using " + osname
            print(colour('green', text))
            replist.append(text)
        else:
            text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
            print(colour('red', text))
            replist.append(text)
elif "Debian" in osname:
    if "8." or "9." in osname:
        text = "Nice work! You are using " + osname
        print(colour('green', text))
        replist.append(text)
    else:
        text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
        print(colour('red', text))
        replist.append(text)
elif "Oracle" in osname:
    splitname = re.split('(\d+)', osname)
    if splitname[1] > 7.29 and splitname[1] < 8:
        text = "Nice work! You are using " + osname
        print(colour('green', text))
        replist.append(text)
    elif splitname[1] > 6.79 and splitname[1] < 7:
        text = "Uh oh, you are using " + osname + ". This is not recommended for new installs"
        print(colour('blue', text))
        replist.append(text)
    else:
        text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
        print(colour('red', text))
        replist.append(text)
elif "Amazon Linux" in osname and "Amazon Linux 2" not in osname:
    splitname = re.split('(\d+)', osname)
    if splitname[1] > 2017.029 and splitname[1] < 2018.031:
        text = "Nice work! You are using " + osname
        print(colour('green', text))
        replist.append(text)
    else:
        text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
        print(colour('red', text))
        replist.append(text)
elif "SuSE" in osname:
    splitname = re.split('(\d+)', osname)
    print(splitname)
    # 12 sp2 and up
    # if splitname[1] >= 12  and "SP" in :
    #     text = "Nice work! You are using " + osname
    #     print(colour('green', text))
    #     replist.append(text)
    # else:
    #     text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
    #     print(colour('red', text))
    #     replist.append(text)
elif "Amazon Linux 2" in osname:
    text = "Uh oh, you are using " + osname + ". We currently only offer experimental support for this OS"
    print(colour('blue', text))
else:
    text = "Uh oh, you are using " + osname + ". We do not currently support this OS"
    print(colour('red', text))
    replist.append(text)
