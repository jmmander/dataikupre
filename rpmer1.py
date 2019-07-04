#!/usr/bin/python

import rpm


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
    return "************************************************\n          Dataiku pre-installation report\n************************************************\n\n   Making sure all your eggs are in the nest!         \n\n"


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
                    print(good(inpkg))
                elif x / (len(wclist)) == len(instpkg):
                    if len(wclist) == numwc:
                        for wcpkg in wclist:
                            if wcpkg not in success:
                                nomissing += 1
                                print(fail(wcpkg, wclist))
                    else:
                        continue
        else:
            if req in instpkg:
                print(good(req))
            else:
                nomissing += 1
                print(fail(req, wclist))
    return nomissing

def fail(req, wclist):
    if req in wclist:
        nokay = req + "* is not installed"
    else:
        nokay = req + " is not installed"
    return (bcolors.FAIL + nokay + bcolors.ENDC)


def good(req):
    okay = req + (" is installed")
    return (bcolors.OKGREEN + okay + bcolors.ENDC)


print(bird())
print(intro())
checkforstuff(prereqs, makedict(), wccount(prereqs))

def total(nomissing):
    if nomissing == len(prereqs):
        return"Uh oh! Looks like the python ate all the eggs in your nest :("
    elif nomissing > 0:
        return "Uh oh! Looks like the python ate " + nomissing + " eggs! :("
    else:
        return "Look at you go! You have all your eggs and are ready to start hatching :)"