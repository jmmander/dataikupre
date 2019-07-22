#!/usr/bin/python3.6
# Description: This script will check for Dataiku 5.1 X pre-requisites
# Author: Jacqueline Mander with guidance from Alex Kaos
# Date: 10/7/19
# Version: 2


import rpm
import os
import subprocess
import re
import shlex
import operator
replist = []






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




def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC + "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "\n\t(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC + "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC + "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC + "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t"


def intro():
    return "**************************************************\n          Dataiku pre-installation report\n**************************************************\n\n   Making sure all your eggs are in the nest...         \n"


prereqs = ["pkg", "httr", "RJSONIO", "dplyr", "sparklyr", "ggplot2", "tidyr", "repr", "evaluate", "IRdisplay", "pbdZMQ", "crayon", "jsonlite", "uuid", "digest", "gtools"]
#hadoop pres = ["hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive","hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*", "java-1.8*"]
#prereqs = ["java-1.8*"]



def makedict():
    instpkg = {}
    ts = rpm.TransactionSet()
    plist = ts.dbMatch()
    for pkg in plist:
        instpkg[pkg['name']] = pkg['version']
    return instpkg


def wccount(prereqs):
    numwc = 0
    for req in prereqs:
        if "*" in req:
            numwc += 1
    return numwc


def checkforstuff(prereqs, instpkg, numwc):
    x = 0
    nomissing = 0
    wclist = []
    success = []
    for req in prereqs:
        if "*" in req:
            pkg = req[:-1]
            wclist.append(pkg)
            for inpkg in instpkg:
                x += 1
                if pkg == inpkg[0:len(pkg)]:
                    success.append(pkg)
                    print(good(inpkg, replist))
                elif x / (len(wclist)) == len(instpkg):
                    if len(wclist) == numwc:
                        for wcpkg in wclist:
                            if wcpkg not in success:
                                nomissing += 1
                                print(fail(wcpkg, wclist, replist))
                    else:
                        continue
        else:
            if req in instpkg:
                print(good(req, replist))
            else:
                nomissing += 1
                print(fail(req, wclist, replist))
    return nomissing

def colour(colour, text):
    if colour == 'red':
        return "* " + (bcolors.FAIL + text + bcolors.ENDC)
    elif colour == 'green':
        return "* " + (bcolors.OKGREEN + text + bcolors.ENDC)
    elif colour == 'white':
        return (bcolors.WHITE + text + bcolors.ENDC)
    elif colour == 'bold':
        return (bcolors.BOLD + text + bcolors.ENDC)




def fail(req, wclist,replist):
    if req in wclist:
        nokay = "Uh oh! " + req + "* is missing from the nest"
        replist.append(nokay)
    else:
        nokay = "Uh oh! " + req + " is missing from the nest"
        replist.append(nokay)
    return colour('red', nokay)


def good(req,replist):
    okay = "Nice work! " +req + (" is safe in the nest")
    replist.append(okay)
    return colour('green', okay)

def result(nomissing):
    if nomissing == str(len(prereqs)):
        return("Uh oh! Looks like you have no eggs in your nest :(")
    elif nomissing > 1:
        return("Uh oh! Looks like you are missing " + str(nomissing) + " eggs! :(")
    elif nomissing == 1:
        return("Uh oh! Looks like you are missing " + str(nomissing) + " egg! :(")
    else:
        return("Look at you go! You have all your eggs and are ready to start hatching :)")



def nest():
    return "   Checking the integrity of your nest..."

#Running on a system with Security-Enhanced Linux (SELinux) in enforcing mode is not supported.
def selinux():
    process = subprocess.Popen(['getenforce'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "Enabled"
    byteword = word.encode(encoding='UTF-8')
    if byteword in stdout:
        nokay = "Uh oh! Your nest has SELinux enabled. "
        fix = "To disable it please edit /etc/selinux/config accordingly and restart the sever"
        replist.append(nokay)
        print(colour('red',nokay) + colour('white',fix))
        return (0,1)
    else:
        okay = "Nice work! Your nest does not have SELinux enabled"
        replist.append(okay)
        print(colour('green',okay))
        return (1,1)






#A minimum of 16 GB of RAM is required. More RAM will be required if you intend to load large datasets in memory (for example in the Jupyter notebook component), or for accomodating more users.
def ram():
    with open('/proc/meminfo') as mem:
        memory = mem.readline()
        nmem = re.sub("[^0-9]", "", memory)
        num = float(nmem)
        gb = round((num/(1024*1024)),2)
        okay = "Your nest is nice and roomy, you have " + str(gb) + "GB" + " of RAM"
        nokay = "Uh oh! Your nest is a little small, you only have " + str(gb) + "GB" + " of RAM "
        if gb < 16:
            replist.append(nokay)
            print(colour('red',nokay))
            return (0,1)
        else:
            replist.append(okay)
            print(colour('green', okay))
            return (1,1)


        mem.closed



#The hard limit on the maximum number of open files for the Unix user account running DSS should be at least 65536 (ulimit -Hn). For very large DSS instances, larger values may be required.
def openfiles():
    process = subprocess.Popen(["ulimit -Hn"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = str(stdout_val[0])
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " files open."
        replist.append(okay)
        print(colour('green', okay))
        return (1,1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " files open. "
        fix = colour('bold', "Please increase it to 65536 or more")
        replist.append(nokay)
        print(colour('red', nokay) + colour('white',fix))
        return (0,1)



#The hard limit on the maximum number of user processes for the Unix user account running DSS should be at least 65536 (ulimit -Hu). For very large DSS instances, larger values may be required.
def userprocesses():
    process = subprocess.Popen(["ulimit -Hu"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = str(stdout_val[0])
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " processes running."
        replist.append(okay)
        print(colour('green',okay))
        return (1,1)
    else:
        nokay = "Uh oh! You can only have " + str(hardlimit) + " processes running. "
        fix = colour('bold',"Please increase it to 65536 or more")
        replist.append(nokay)
        print(colour('red', nokay) + colour('white',fix))
        return (0,1)


#The en_US.utf8 locale must be installed.
def locale():
    process = subprocess.Popen(['locale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "en_US.UTF-8"
    byteword = word.encode(encoding='UTF-8')
    if byteword in stdout:
        okay = "Nice work! You are using en_US.utf8"
        replist.append(okay)
        print(colour('green',okay))
        return (1,1)
    else:
        nokay = "Uh oh! You are not using en_US.utf8"
        replist.append(nokay)
        print(colour('red', nokay))
        return (0,1)


def nester():
    a = selinux()
    b = ram()
    c = openfiles()
    d = userprocesses()
    e = locale()
    total = tuple(map(sum, zip(a, b, c, d, e)))
    nestnum = total[1] - total[0]
    return nestnum




def report(replist):
    with open('dku-report.txt', 'w+') as report:
        for item in replist:
            report.write("%s\n" % item)
        report.closed
    #with open('dku-report.txt', 'r') as reading:
     #   print(reading.read())
      #  reading.closed

def ending(nomissing, nestnum):

    if nomissing == 0 and nestnum == 0:
        return "Congratuations! Your nest is sound and all your eggs in place. Dataiku is ready to take flight! " + fly()
    elif nomissing == 0 and nestnum != 0:
        return "You have all your eggs but your nest isn't quite ready! Please make the necessary changes so Dataiku can take flight"
    elif nomissing > 1 and nestnum == 0:
        return "Your nest is sound but you're missing an egg or two! Please download the missing packages so Dataiku can take flight"
    else:
        return "Oh dear! Your missing some eggs and your nest is not yet sound. Please download the missing packages and make the necessary changes so Dataiku can take flight"

def fly():
    return "\n\n\t          @\n\t          @@\n\t         @@@@   \n\t   @@@@@@@@@@@    @@@  \n\t    @@@@@@@@@@@@@@@@@@>\n\t      @@@@@@@@@@@@@@@  \n\t        @@@@@@@@@@@@   \n\t    @@@@@@@@@@@@@"




print(bird())
print(intro())
num = checkforstuff(prereqs, makedict(), wccount(prereqs))
print("\n"+str(result(num))+ "\n\n")
print(nest() + "\n")
print("\n" + ending(num, nester()) +"\n\n")

report(replist)



