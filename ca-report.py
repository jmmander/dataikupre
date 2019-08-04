#!/usr/bin/python
# Description: This script will check for Dataiku DSS 5.1 X pre-requisites
# Author: Jacqueline Mander with guidance from Alex Kaos
# Date: 1/8/19
# Version: 2.5


import rpm
import os
import subprocess
import re
import shlex
import operator
import datetime
import platform
from sys import stdout

replist = []
wc_dic = {}



# required version of python, numbers only
pyver = "2.7"

r_prereqs = ["pkg", "httr", "RJSONIO", "dplyr", "sparklyr", "ggplot2", "tidyr", "repr", "evaluate", "IRdisplay",
             "pbdZMQ", "crayon", "jsonlite", "uuid", "digest", "gtools"]

hadoop_prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive",
                  "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*"]

dss_prereqs = ["java-1.8", "acl", "expat", "git", "zip", "unzip", "nginx", "freetype", "libgfortran", "libgomp",
               "freetype", "libgfortran", "libgomp", "python-devel", "bzip2", "mesa-libGL", "libSM", "libXrender",
               "libgomp", "alsa-lib", "R-core-devel", "libicu-devel", "libcurl-devel", "openssl-devel", "libxml2-devel",
               "zeromq-devel", "libssh2-devel", "openldap-devel", "tomcat-*"]

prereqs = dss_prereqs + r_prereqs + hadoop_prereqs


# creates text formatting classes
class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[99m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# applies text formatting
def colour(colour, text):
    if colour == 'red':
        return "* " + (bcolors.FAIL + text + bcolors.ENDC)
    elif colour == 'green':
        return "* " + (bcolors.OKGREEN + text + bcolors.ENDC)
    elif colour == 'white':
        return (bcolors.WHITE + text + bcolors.ENDC)
    elif colour == 'bold':
        return (bcolors.BOLD + text + bcolors.ENDC)
    elif colour == "blue":
        return "* " + (bcolors.CYAN + text + bcolors.ENDC)
    elif colour == "yellow":
        return "* " + (bcolors.WARNING + text + bcolors.ENDC)


# checks for root user privileges
def sudo():
    if os.geteuid() != 0:
        exit("Uh oh! You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.")


# returns dataikju bird logo
def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC + "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "\n\t(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC + "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC + "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC + "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t"


# introduction
def intro():
    return "**************************************************\n       Dataiku DSS pre-installation report\n**************************************************\n\n   Checking all your eggs are in the nest...         \n  ------------------------------------------- \n"


# checks which packages are avaiable
def avail(prereqs):
    av = []
    p1 = subprocess.Popen(['yum', 'list', 'available'], stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    for pkg in prereqs:
        if "*" in pkg:
            wildcard(pkg, output, "ava", wc_dic)
        else:
            pattern = '(?<!\\S)' + pkg + '[^a-zA-Z]'
            stringpat = str(pattern)
            result = re.findall(stringpat, output)
            if result:
                av.append(pkg)
            else:
                continue
    return av



# checks which packages are installed
def installed(prereqs):
    ins = []
    p1 = subprocess.Popen(['yum', 'list', 'installed'], stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    for pkg in prereqs:
        if "*" in pkg:
            wildcard(pkg, output, "inst", wc_dic)
        else:
            pattern = '(?<!\\S)' + pkg + '[^a-zA-Z]'
            stringpat = str(pattern)
            result = re.findall(stringpat, output)
            if result:
                ins.append(pkg)
            else:
                continue
    return ins

#returns dictionary of  wildcard results
def wildcard(pkg, output, inav, wc_dic):
    pname = pkg[:-1]
    pattern = '(?<!\\S)' + pname + '\w+'
    stringpat = str(pattern)
    result = re.findall(stringpat, output)
    if result:
        if inav == "inst":
            for pack in result:
                if pack not in wc_dic:
                    wc_dic[pack] = "installed"
        else:
            for pack in result:
                if pack not in wc_dic:
                    wc_dic[pack] = "available"
    else:
        if pkg not in wc_dic:
            wc_dic[pkg] = "not-available"
    return wc_dic







# returns all missing packages (not available or installed)
def missing(prereqs, av, ins):
    combo = av + ins
    unique = set(combo)
    notin = set(prereqs) - unique
    return notin


# prints package check results
def echo(prereqs, ins, av, wc_dic):
    for pkg in prereqs:
        if "*" not in pkg:
            if pkg in ins:
                yayay = (pkg + " is installed")
                repdic("inst", pkg)
                print(colour("green", yayay))
            elif pkg in av:
                soso = (pkg + " is available but not installed")
                repdic("avail", pkg)
                print(colour("blue", soso))
            else:
                nono = (pkg + " is not available")
                repdic("notav", pkg)
                print(colour("red", nono))
    for pack in wc_dic:
        if wc_dic[pack] == "installed":
            yayay = (pack + " is installed")
            repdic("inst", pack)
            print(colour("green", yayay))
        elif wc_dic[pack] == "available":
            soso = (pack + " is available but not installed")
            repdic("avail", pack)
            print(colour("blue", soso))
        else:
            nono = (pack + " is not available")
            repdic("notav", pack)
            print(colour("red", nono))






# returns results of just the packages
# def result(nomissing):
#     if nomissing == str(len(prereqs)):
#         return ("Uh oh! Looks like you have no eggs in your nest :(")
#     elif nomissing > 1:
#         return ("Uh oh! Looks like you are missing " + str(nomissing) + " eggs! :(")
#     elif nomissing == 1:
#         return ("Uh oh! Looks like you are missing " + str(nomissing) + " egg! :(")
#     else:
#         return ("Look at you go! You have all your eggs and are ready to start hatching :)")


def nest():
    return "\n\n    Checking the integrity of your nest...\n   ---------------------------------------- \n"


# checks python version
def python():
    python_version = platform.python_version()
    if pyver in python_version:
        okay = "Nice work! You have python" + python_version
        repdic("req-met", python_version)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You have " + python_version
        replist.append(nokay)
        fix = "DSS only works with python" + pyver
        repdic("req-not-met", python_version)
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)


# checks if system can connect to r repo
def ping():
    hostname = "cran.cnr.berkeley.edu"
    response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        text = 'Nice work! You can connect to ' + hostname
        repdic("req-met", hostname)
        print(colour('green', text))
        return (1, 1)
    else:
        text = "Uh oh! You can\'t connect to " + hostname
        repdic("req-not-met", hostname)
        print(colour('red', text))
        return (0, 1)


# checks if system has Security-Enhanced Linux (SELinux) in enforcing mode
def selinux():
    process = subprocess.Popen(['getenforce'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "Enabled"
    #for python 3: byteword = word.encode(encoding='UTF-8')
    if word in stdout:
        nokay = "Uh oh! Your nest has SELinux enabled. "
        fix = "To disable it please edit /etc/selinux/config accordingly and restart the sever"
        repdic("req-not-met","SELinux")
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)
    else:
        okay = "Nice work! Your nest does not have SELinux enabled"
        repdic("req-met","SELinux")
        print(colour('green', okay))
        return (1, 1)


# checks amount of RAM available
def ram():
    with open('/proc/meminfo') as mem:
        memory = mem.readline()
        nmem = re.sub("[^0-9]", "", memory)
        num = float(nmem)
        gb = round((num / (1024 * 1024)), 2)
        okay = "Your nest is nice and roomy, you have " + str(gb) + "GB" + " of RAM"
        nokay = "Uh oh! Your nest is a little small, you only have " + str(gb) + "GB" + " of RAM "
        if gb < 16:
            repdic("req-not-met", str(gb) + "GB RAM")
            print(colour('red', nokay))
            return (0, 1)
        else:
            repdic("req-met", str(gb) + "GB RAM")
            print(colour('green', okay))
            return (1, 1)

        mem.closed


# Checks the hard limit on the maximum number of open files for the Unix user account running DSS
def openfiles():
    process = subprocess.Popen(["ulimit -Hn"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = str(stdout_val[0])
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " files open."
        repdic("req-met", str(hardlimit) + " files open")
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " files open. "
        fix = colour('bold', "Please increase it to 65536 or more")
        repdic("req-not-met", str(hardlimit) + " files open")
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)


# Checks the hard limit on the maximum number of user processes for the Unix user account running DSS
def userprocesses():
    process = subprocess.Popen(["ulimit -Hu"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = str(stdout_val[0])
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " processes running."
        repdic("req-met", str(hardlimit) + "  processes running")
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " processes running. "
        fix = colour('bold', "Please increase it to 65536 or more")
        repdic("req-not-met", str(hardlimit) + "  processes running")
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)


# checks if en_US.utf8 locale is installed.
def locale():
    process = subprocess.Popen(['localectl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "en_US.UTF-8"
    # byteword = word.encode(encoding='UTF-8')
    if word in stdout:
        okay = "Nice work! You are using en_US.utf8"
        repdic("req-met", word)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You are not using en_US.utf8"
        repdic("req-not-met", word)
        print(colour('red', nokay))
        return (0, 1)


# calls all system related checks and returns tuple
def nester():
    f = python()
    a = selinux()
    b = ram()
    c = openfiles()
    d = userprocesses()
    e = locale()
    g = ping()
    total = tuple(map(sum, zip(a, b, c, d, e, f, g)))
    nestnum = total[1] - total[0]
    return nestnum


# uses tuple from nester to provide results
def ending(nomissing, nestnum):
    if nomissing == 0 and nestnum == 0:
        text = "Congratuations! You have all the necessary requirements. Dataiku DSS is ready to take flight!"
        return "\n" + colour("bold", text) + "\n\n\n" + fly()
    elif nomissing == 0 and nestnum != 0:
        text = "You have all your eggs but your nest isn't quite ready! Please make the necessary changes so Dataiku DSS can take flight"
        return "\n" + colour("bold", text) + "\n\n\n" + almost()
    elif nomissing > 0 and nestnum == 0:
        text = "Your nest is sound but you're missing an egg or two! Please download the missing packages so Dataiku DSS can take flight"
        return "\n" + colour("bold", text) + "\n\n\n" + almost()
    else:
        text = "Oh dear! You're missing some eggs and your nest is not yet sound. Please download the missing packages and make the necessary changes so Dataiku DSS can take flight"
        return "\n" + colour("bold", text) + "\n\n\n" + almost()

def repdic(status, name, reportdic = {}):
    for status,name in reportdic:
        if name not in reportdic:
            if status == "inst":
                reportdic[name] = "installed"
            elif status == "avail":
                reportdic[name] = "available"
            elif status == "notavail":
                reportdic[name] = "notavailable"
            elif status == "met":
                reportdic[name] = "req-met"
            else:
                reportdic[name] = "req-not-met"
    print(reportdic)
    return reportdic





# creates new file with results
def report(reportdic):
    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d-%H:%M")
    name = 'dku-preinstall-report-' + dt + '.txt'
    with open(name, 'w+') as report:
        report.write("PACKAGES:\n\nINSTALLED:\n")
        for key, name in reportdic:
            if key == "installed":
                report.write("%s\n" %name)
        report.write("\n\nAVAILABLE:\n")
        for key, name in reportdic:
            if key == "available":
                report.write("%s\n" %name)
        report.write("\n\nNOT AVAILABLE:\n")
        for key, name in reportdic:
            if key == "notavailable":
                report.write("%s\n" %name)
        report.write("\n\n\n\nSYSTEM REQUIREMENTS:\n\nMET:\n")
        for key, name in reportdic:
            if key == "req-met":
                report.write("%s\n" %name)
        report.write("\n\nNOT MET:\n")
        for key, name in reportdic:
            if key == "req-not-met":
                report.write("%s\n" %name)

        report.closed
    print(name + ' has been created\n')


# bird trying to fly
def almost():
    return (
        "      .---.        .-----------\n     /     \\  __  /    ------\n    / /     \\(  )/    -----\n   //////   \' \\/ `   ---\n  //// / // :    : ---\n // /   /  `    \'--\n//          //..\\\\\n       ====UU====UU====\n           \'//||\\\\`\n             \'\'``\n")


# bird flying
def fly():
    return (
        "                                 .ze$$e.\n              .ed$$$eee..      .$$$$$$$P\"\"\"\n           z$$$$$$$$$$$$$$$$$ee$$$$$$\"\n        .d$$$$$$$$$$$$$$$$$$$$$$$$$\"\n      .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$e..\n    .$$****\"\"\"\"***$$$$$$$$$$$$$$$$$$$$$$$$$$$be.\n                     \"\"**$$$$$$$$$$$$$$$$$$$$$$$L\n                       z$$$$$$$$$$$$$$$$$$$$$$$$$\n                     .$$$$$$$$P**$$$$$$$$$$$$$$$$\n                    d$$$$$$$\"              4$$$$$\n                  z$$$$$$$$$                $$$P\"\n                 d$$$$$$$$$F                $P\"\n                 $$$$$$$$$$F\n                  *$$$$$$$$\"\n                    \"***\"\"\n")


sudo()
print(bird())
print(intro())
installed(prereqs)
avail(prereqs)
echo(prereqs, avail(prereqs), installed(prereqs), wc_dic)
# result(len(missing(prereqs, av, ins)))
print(nest())
print("\n" + ending(len(missing(prereqs, avail(prereqs), installed(prereqs))), nester()) + "\n\n")
report(repdic("status", "name"))


