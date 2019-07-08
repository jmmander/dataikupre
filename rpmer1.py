#!/usr/bin/python

import rpm
import os
import subprocess
import re
import shlex
replist = []




class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'




def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC + "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "\n\t(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC + "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC + "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC + "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC + "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC + "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC + "@@@@@@@@\n\t"


def intro():
    return "**************************************************\n          Dataiku pre-installation report\n**************************************************\n\n   Making sure all your eggs are in the nest!         \n\n"


prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive",
           "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*", "java-1.8*"]


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

def red(text):
    return (bcolors.FAIL + text + bcolors.ENDC)

def green(text):
    return (bcolors.OKGREEN + text + bcolors.ENDC)

def fail(req, wclist,replist):
    if req in wclist:
        nokay = req + "* is missing from the nest"
        replist.append(nokay)
    else:
        nokay = req + " is missing from the nest"
        replist.append(nokay)
    return red(nokay)


def good(req,replist):
    okay = req + (" is safe in the nest")
    replist.append(okay)
    return green(okay)

def result(nomissing):
    if nomissing == str(len(prereqs)):
        return"Uh oh! Looks like you have no eggs in your nest :("
    elif nomissing > 1:
        return "Uh oh! Looks like you are missing " + str(nomissing) + " eggs! :("
    elif nomissing == 1:
        return "Uh oh! Looks like you are missing " + str(nomissing) + " egg! :("
    else:
        return "Look at you go! You have all your eggs and are ready to start hatching :)"




#Running on a system with Security-Enhanced Linux (SELinux) in enforcing mode is not supported.
def selinux():
    process = subprocess.Popen(['getenforce'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if "Disabled" in stdout:
        okay = "Nice work! Your nest does not have SELinux enabled"
        replist.append(okay)
        return green(okay)
    else:
        nokay = "Uh oh! Your nest has SELinux enabled"
        replist.append(nokay)
        return red(nokay)





#A minimum of 16 GB of RAM is required. More RAM will be required if you intend to load large datasets in memory (for example in the Jupyter notebook component), or for accomodating more users.
def ram():
    with open('/proc/meminfo') as mem:
        memory = mem.readline()
        nmem = re.sub("[^0-9]", "", memory)
        num = float(nmem)
        gb = round((num/(1024*1024)),2)
        okay = "Your nest is nice and roomy, you have " + str(gb) + "GB" + " of space."
        nokay = "Uh oh! Your nest is a little small, you only have " + str(gb) + "GB" + " of space."
        if gb < 16:
            replist.append(nokay)
            return(red(nokay))
        else:
            replist.append(okay)
            return(green(okay))

        mem.closed



#The hard limit on the maximum number of open files for the Unix user account running DSS should be at least 65536 (ulimit -Hn). For very large DSS instances, larger values may be required.
def openfiles():
    process = subprocess.Popen(["ulimit -Hn"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = stdout_val[0]
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " files open."
        replist.append(okay)
        return green(okay)
    else:
        nokay = "Uh oh! Your nest can only have " + str(hardlimit) + " files open."
        replist.append(nokay)
        return red(nokay)



#The hard limit on the maximum number of user processes for the Unix user account running DSS should be at least 65536 (ulimit -Hu). For very large DSS instances, larger values may be required.
def userprocesses():
    process = subprocess.Popen(["ulimit -Hu"], shell=True, stdout=subprocess.PIPE)
    stdout_val = process.communicate()
    num = stdout_val[0]
    lim = re.sub("[^0-9]", "", num)
    hardlimit = int(lim)
    if hardlimit >= 65536:
        okay = "Nice work! Your nest can have " + str(hardlimit) + " processes running."
        replist.append(okay)
        return green(okay)
    else:
        nokay = "Uh oh! Your nest can only have " + str(hardlimit) + " processes running."
        replist.append(nokay)
        return red(nokay)


#The en_US.utf8 locale must be installed.
def locale():
    process = subprocess.Popen(['locale'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if "en_US.UTF-8" in stdout:
        okay = "Nice work! You are using en_US.utf8"
        replist.append(okay)
        return green(okay)
    else:
        nokay = "Uh oh! You are not using en_US.utf8"
        replist.append(nokay)
        return red(nokay)


def report(replist):
    with open('dku-report.txt', 'w+') as report:
        for item in replist:
            report.write("%s\n" % item)
        report.closed
    #with open('dku-report.txt', 'r') as reading:
     #   print(reading.read())
      #  reading.closed

print(bird())
print(intro())
num = checkforstuff(prereqs, makedict(), wccount(prereqs))
print("\n\n"+result(num)+ "\n\n")
print(selinux())
print(ram())
print(openfiles())
print(userprocesses())
print(locale())
report(replist)



