#!/usr/bin/python
# Description: This script will check for Dataiku DSS 5.1 X pre-requisites
# Primary developer: Jacqueline Mander
# Primary designer: Alex Kaos
# Date: 6/8/19
# Version: 2.9


import os
from os import geteuid
from os import system
from os import name
import subprocess
import re
import shlex
import operator
import datetime
import platform
from sys import stdout

replist = []
wc_dic = {}


#number of CPU cores required
cpucore = 4

#hardlimit for system
ulimit = 65536

# required version of python, numbers only
pyver = "2.7"


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
    if geteuid() != 0:
        exit("Uh oh! You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.")


# returns dataikju bird logo
def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC + "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "\n\t(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC + "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC + "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC + "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t"


# introduction
def intro():
    return "**************************************************\n       Dataiku DSS pre-installation report\n**************************************************\n\n   " \

#asks questions to user
def questionasker(addon, list):
    while True:
        ans = raw_input(bcolors.OKGREEN + "  Will you be using " + addon +"? (y/n): " + bcolors.ENDC)
        if ans.lower() == "y" or ans.lower() == "yes":
            return addon
        elif ans.lower() == "n" or ans.lower() =="no":
            return None
        else:
            print("  Oopsies! We didn't quite understand that. Please try again answering with either 'y' or 'n'")


#builds custom list of prereq packages based off customers response
def prebuilder():
    r_prereqs = ["zeromq-devel", "libssh2-devel", "openldap-devel", "R-core-devel", "libicu-devel", "libcurl-devel",
                 "openssl-devel", "libxml2-devel", "pkg", "httr", "RJSONIO", "dplyr", "sparklyr", "ggplot2", "tidyr",
                 "repr", "evaluate", "IRdisplay",
                 "pbdZMQ", "crayon", "jsonlite", "uuid", "digest", "gtools", "zeromq-devel", "libssh2-devel",
                 "openldap-devel"]

    hadoop_prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus",
                      "hive",
                      "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*"]

    dss_prereqs = ["java-1.8", "acl", "expat", "git", "zip", "unzip", "nginx", "libgfortran", "libgomp",
                   "freetype", "libgomp", "python-devel"]

    conda_prereqs = ["bzip2", "mesa-libGL", "libSM", "libXrender", "alsa-lib"]

    prereqs = dss_prereqs
    print("Just a few quick questions before we begin...\n")
    if questionasker("Hadoop", hadoop_prereqs) == "Hadoop":
        prereqs = prereqs + hadoop_prereqs
    if questionasker("R", r_prereqs) == "R":
        prereqs = prereqs + r_prereqs
    if questionasker("Anaconda", conda_prereqs) == "Anaconda":
        prereqs = prereqs + conda_prereqs
    print("\nThank you! Now on with the show...\n\n")
    return prereqs

def eggs():
    return "\n\n   Checking all your eggs are in the nest...         \n  ------------------------------------------- \n"


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
    #retirns twice, need to check if in ins
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
    nowc = []
    combo = av + ins
    unique = set(combo)
    for pkg in prereqs:
        if "*" not in pkg:
            nowc.append(pkg)
    notin = set(nowc) - unique
    return notin


# prints package check results
def echo(notin, ins, av, wc_dic):
    avanotin = []
    for pkg in av:
        if pkg not in ins:
            avanotin.append(pkg)
    for pkg in ins:
        yayay = (pkg + " is installed")
        replist.append(yayay)
        print(colour("green", yayay))
    for pack in wc_dic:
        if wc_dic[pack] == "installed":
            yayay = (pack + " is installed")
            replist.append(yayay)
            print(colour("green", yayay))
    for pkg in avanotin:
        soso = (pkg + " is available but not installed")
        print(colour("blue", soso))
    for pack in wc_dic:
        if wc_dic[pack] == "available":
            soso = (pack + " is available but not installed")
            replist.append(soso)
            print(colour("blue", soso))
    for pkg in notin:
        nono = (pkg + " is not available")
        replist.append(nono)
        print(colour("red", nono))
    for pack in wc_dic:
        if wc_dic[pack] == "not-available":
            nono = (pack + " is not available")
            replist.append(nono)
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
        okay = "Nice work! You have python " + python_version
        replist.append(okay)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You have " + python_version
        replist.append(nokay)
        fix = "DSS only works with python " + pyver
        replist.append(nokay)
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)



#checks is OS is supported as per DSS documentation
def os():
    print("   Checking the habitability of your environment...\n  ---------------------------------------------------\n")
    with open ('/etc/os-release') as os:
        osnamelist = os.readlines()
        for line in osnamelist:
            if "PRETTY" in line:
                osname = re.findall("[\"].*?[\"]", line)
                print(osname)

    #p1 = subprocess.Popen(['cat', '/etc/os-release'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout = p1.communicate()
    # stroutput = str(stdout)
    # result = re.search('PRETTY_NAME="(.*?)"', stroutput)
    # osname = (result.group(1))
    if "Red Hat" in osname:
        redhat(osname)
    elif "CentOS" in osname:
        centos()

def redhat(osname):
    gpattern = "7(\.[3-9])"
    bpattern = "6(\.[8-9])"
    good = re.findall(gpattern, osname)
    if good:
        text = (osname + " is being used. This is fully supported in the 64bit version only.")
        print(colour("green",text))
        replist.append(text)
    bad = re.findall(bpattern, osname)
    if bad:
        text = (osname + " is being used. This is NOT recommended for new installations")
        print(colour("blue", text))
        replist.append(text)
    if good is False and bad is False:
        text = (osname + " is being used. This is not currently supported.")
        print(colour(text, "red"))
        replist.append(text)

def centos():
    with open ('/etc/centos-release') as cenrel:
        relname = cenrel.readline()
        osname = relname.rstrip()
    gpattern = "7(\.[3-9])"
    bpattern = "6(\.[8-9])"
    good = re.findall(gpattern, osname)
    if good:
        text = (osname + " is being used. This is fully supported in the 64bit version only.")
        print(colour("green", text))
        replist.append(text)
    bad = re.findall(bpattern, osname)
    if bad:
        text = (osname + " is being used. This is NOT recommended for new installations")
        print(colour("blue", text))
        replist.append(text)
    if good == False and bad == False:
        text = (osname + " is being used. This is not currently supported.")
        print(colour(text, "red"))
        replist.append(text)

    # elif "Ubuntu" in osname:
    #     sup = "  The following Linux distributions are fully supported, in 64-bit version only: \n\tUbuntu Server, versions 16.04 LTS and 18.04 LTS"
    # elif "Debian" in osname:
    #     sup = "  The following Linux distributions are fully supported, in 64-bit version only: \n\tDebian, versions 8.x and 9.x"
    # elif "Orcale" in osname:
    #     sup = "  The following Linux distributions are fully supported, in 64-bit version only: \n\tOracle Linux, version 7.3 and later 7.x. \n\n  Oracle Linux 6.8 and later 6.x are NOT reccommended for new installations."
    # elif "Amazon Linux 2" in osname:
    #     sup = "  The following Linux distributions are supported, in 64-bit version only: \n\tAmazon Linux 2 (experimental support only)"
    # elif "Amazon Linux" in osname:
    #     sup = "  The following Linux distributions are fully supported, in 64-bit version only: \n\tAmazon Linux, version 2017.03 and later (tested up to version 2018.03)"
    # elif "SuSE" in osname:
    #     sup = "  The following Linux distributions are fully supported, in 64-bit version only: \n\tSuSE 12 SP2 and later"
    # #print("* " + text + "\n")
    # #if sup:
    #    # print(sup + "\n\n")











# checks if system can connect to r repo
def ping():
    hostname = "cran.cnr.berkeley.edu"
    response = system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        text = 'Nice work! You can connect to ' + hostname
        replist.append(text)
        print(colour('green', text))
        return (1, 1)
    else:
        text = "Uh oh! You can\'t connect to " + hostname
        replist.append(text)
        print(colour('red', text))
        return (0, 1)


# checks if system has Security-Enhanced Linux (SELinux) in enforcing mode
def selinux():
    process = subprocess.Popen(['getenforce'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "Enabled"
    # byteword = word.encode(encoding='UTF-8')
    if word in stdout:
        nokay = "Uh oh! Your nest has SELinux enabled. "
        fix = "To disable it please edit /etc/selinux/config accordingly and restart the sever"
        replist.append(nokay)
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)
    else:
        okay = "Nice work! Your nest does not have SELinux enabled"
        replist.append(okay)
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
            replist.append(nokay)
            print(colour('red', nokay))
            return (0, 1)
        else:
            replist.append(okay)
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
    if hardlimit >= ulimit:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " files open."
        replist.append(okay)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " files open. "
        fix = colour('bold', "Please increase it to " + str(ulimit) + " or more")
        replist.append(nokay)
        print(colour('red', nokay) + colour('white', fix))
        return (0, 1)


# Checks the hard limit on the maximum number of user processes for the Unix user account running DSS
def userprocesses():
    process = subprocess.Popen(["ulimit -Hu"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = str(stdout_val[0])
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= ulimit:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " processes running."
        replist.append(okay)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " processes running. "
        fix = colour('bold', "Please increase it to " + str(ulimit) + " or more")
        replist.append(nokay)
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
        replist.append(okay)
        print(colour('green', okay))
        return (1, 1)
    else:
        nokay = "Uh oh! You are not using en_US.utf8"
        replist.append(nokay)
        print(colour('red', nokay))
        return (0, 1)

#checks number of CPU cores
def cpucores():
    process = subprocess.Popen(['nproc'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    nocores = str(stdout).rstrip()
    nocoresnum = int(nocores)
    if nocoresnum < 4:
        nokay = "Uh oh! You only have " + str(nocoresnum) + " CPU core(s)"
        replist.append(nokay)
        print(colour('red', nokay))
        return (0, 1)
    else:
        okay = "Nice work! You have " + str(nocoresnum) + " CPU cores"
        replist.append(okay)
        print(colour('green', okay))
        return (1, 1)



# calls all system related checks and returns tuple
def nester():
    f = python()
    a = selinux()
    b = ram()
    c = openfiles()
    d = userprocesses()
    e = locale()
    g = ping()
    i = cpucores()
    total = tuple(map(sum, zip(a, b, c, d, e, f, g, i)))
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


# creates new file with results
def report(replist):
    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d-%H:%M")
    name = 'dku-preinstall-report-' + dt + '.txt'
    with open(name, 'w+') as report:
        for item in replist:
            report.write("%s\n" % item)
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
prereqs = prebuilder()
print(bird())
print(intro())
os()
print(eggs())
instpkgs = installed(prereqs)
availpkgs = avail(prereqs)
notin = missing(prereqs, availpkgs, instpkgs)
echo(notin, instpkgs, availpkgs, wc_dic)
# result(len(missing(prereqs, av, ins)))
print(nest())
print("\n" + ending(len(notin), nester()) + "\n\n")
report(replist)



