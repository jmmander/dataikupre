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



def fail(req):
    if req in wclist:
        nokay = req + "* is not installed"
    else:
        nokay = req + " is not installed"
    return (bcolors.FAIL + nokay + bcolors.ENDC)


def good(req):
    okay = req + (" is installed")
    return (bcolors.OKGREEN + okay + bcolors.ENDC)

def bird():
    return "\n\n\t@@@@@@@@@@@@" + bcolors.CYAN + "(((((((((((" + bcolors.ENDC+ "@@@@@@@@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "((((((((((((((((((("+ bcolors.ENDC +"@@@@@@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC+ "@@@@@\n\t@@@" + bcolors.CYAN + "(((((((((((((((((((((((((((((" + bcolors.ENDC+ "@@@\n\t@@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((" + bcolors.ENDC + "@@\n\t@" + bcolors.CYAN + "((((((((((((((((((((" + bcolors.ENDC + "@@@@@" + bcolors.CYAN + "((((((((" + bcolors.ENDC+ "@" + bcolors.CYAN +"\n\t(((((((((((((((((((" + bcolors.ENDC+ "@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((((" + bcolors.ENDC+ "@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((((" + bcolors.ENDC+ "@@@@@@@@@@" + bcolors.CYAN + "(((((((((\n\t((((((((((((((" + bcolors.ENDC+ "@@@@@@@@@@@" + bcolors.CYAN + "((((((((((\n\t(((((((((((((" + bcolors.ENDC+ "@@@@@@@@@" + bcolors.CYAN + "(((((((((((((\n\t(((((((((((" + bcolors.ENDC+ "@@" + bcolors.CYAN + "((((((" + bcolors.ENDC+ "@@@@@@@@@" + bcolors.CYAN + "(((((((\n\t" + bcolors.ENDC + "@" + bcolors.CYAN + "(((((((((" + bcolors.ENDC+ "@" + bcolors.CYAN + "(((((((((((((((((((((((" + bcolors.ENDC+ "@\n\t@@" + bcolors.CYAN + "((((((" + bcolors.ENDC+ "@" + bcolors.CYAN + "((((((((((((((((((((((((" + bcolors.ENDC+ "@@\n\t@@@" + bcolors.CYAN + "(((" + bcolors.ENDC+ "@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC+ "@@@\n\t@@@@@" + bcolors.CYAN + "(((((((((((((((((((((((((" + bcolors.ENDC+ "@@@@@\n\t@@@@@@@@" + bcolors.CYAN + "(((((((((((((((((((" + bcolors.ENDC+ "@@@@@@@@\n\t"

def intro():
    return "************************************************\n          Dataiku pre-installation report\n************************************************\n"

prereqs = ["hadoop-client", "hadoop-lzo", "spark-core", "spark-python", "spark-R", "spark-datanucleus", "hive", "hive-hcatalog", "pig", "tez", "openssl-devel", "emrfs", "emr-*", "java-1.8*"]
instpkg = {}
x= 0
wclist = []
numwc = 0
success = []
print(bird())
print(intro())


ts = rpm.TransactionSet()
plist = ts.dbMatch()
for pkg in plist:
    instpkg[pkg['name']] = pkg['version']


for req in prereqs:
    if "*" in req:
        numwc += 1

for req in prereqs:
    if "*" in req:
        pkg = req[:-1]
        wclist.append(pkg)
        for inpkg in instpkg:
            x += 1
            if pkg == inpkg[0:len(pkg)]:
                success.append(pkg)
                print(good(inpkg))
            elif x/(len(wclist)) == len(instpkg):
                if len(wclist) == numwc:
                    for wcpkg in wclist:
                        if wcpkg not in success:
                            print(fail(wcpkg))
            else:
                continue
    else:
        if req in instpkg:
            print(good(req))
        else:
            print(fail(req))



