#!/usr/bin/python
# Description: This script will check for Dataiku DSS 5.1 X pre-requisites
# Author: Jacqueline Mander with guidance from Alex Kaos
# Date: 10/7/19
# Version: 2


import rpm
import os
import subprocess
import re
import shlex
import operator
import datetime
replist = []
notin = []






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




#R pres
prereqs = ["pkg", "httr", "RJSONIO", "dplyr", "sparklyr", "ggplot2", "tidyr", "repr", "evaluate", "IRdisplay", "pbdZMQ", "crayon", "jsonlite", "uuid", "digest", "gtools"]

#hadoop prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive","hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*", "java-1.8*"]
#other prereqs = ["java-1.8*"]



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


def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC + "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "\n\t(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC + "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC + "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC + "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t"

def intro():
    return "**************************************************\n          Dataiku DSS pre-installation report\n**************************************************\n\n   Checking all your eggs are in the nest...         \n"

def avail(prereqs):
    process = subprocess.Popen(['yum', 'list', 'available'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    for pkg in prereqs:
        if pkg in stdout:
            installed(pkg)
        else:
            nono = (pkg + " is not available")
            replist.append(nono)
            notin.append(pkg)
            print(colour("red", nono))


def installed(pkg):
    process = subprocess.Popen(['yum', 'list', 'installed'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if pkg in stdout:
        yayay = (pkg + " is installed")
        replist.append(yayay)
        print(colour("green", yayay))
    else:
        soso = (pkg + " is available but not installed")
        replist.append(soso)
        print(colour("blue", soso))

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
    return "\n\n    Checking the integrity of your nest...\n"


#Running on a system with Security-Enhanced Linux (SELinux) in enforcing mode is not supported.
def selinux():
    process = subprocess.Popen(['getenforce'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    word = "Enabled"
    #byteword = word.encode(encoding='UTF-8')
    if word in stdout:
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
    #byteword = word.encode(encoding='UTF-8')
    if word in stdout:
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


def ending(nomissing, nestnum):
    if len(notin) == 0 and nestnum == 0:
        return "Congratuations! You have all the necessary requirements. Dataiku DSS is ready to take flight! "
    elif len(notin) == 0 and nestnum != 0:
        return "You have all your eggs but your nest isn't quite ready! Please make the necessary changes so Dataiku DSS can take flight"
    elif len(notin) > 0 and nestnum == 0:
        return "Your nest is sound but you're missing an egg or two! Please download the missing packages so Dataiku DSS can take flight"
    else:
        return "Oh dear! You're missing some eggs and your nest is not yet sound. Please download the missing packages and make the necessary changes so Dataiku DSS can take flight"



def report(replist):
    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d-%H:%M")
    name = 'dku-avail-report-' + dt + '.txt'
    with open(name, 'w+') as report:
        for item in replist:
            report.write("%s\n" % item)
        report.closed
    print(name + ' has been created\n')
        
        
print(bird())
print(intro().upper())
avail(prereqs)
result(len(notin))
print(nest().upper())
print("\n" + ending(len(notin), nester()) +"\n\n")
report(replist) 








